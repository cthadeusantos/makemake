from django.contrib.auth import logout
from django.utils.timezone import now

from auditlog.context import set_actor
from makemake.core.custom_functions import get_client_ip

class AuditlogUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Define o usuário autenticado como ator
            set_actor(request.user)
        response = self.get_response(request)
        return response

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Configura o IP no contexto do auditlog
        ip = get_client_ip(request)
        if request.user.is_authenticated:
            with set_actor(request.user, remote_addr=ip):
                pass

"""
Logout automático por inatividade no Django
"""
class InactivityLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                # Converte a string de volta para datetime, se necessário
                if isinstance(last_activity, str):
                    from datetime import datetime
                    last_activity = datetime.fromisoformat(last_activity.replace('Z', '+00:00')) # Ajuste para timezone UTC

                now_time = now()
                inactive_time = now_time - last_activity
                if inactive_time.total_seconds() > 900:
                    logout(request)

            # Formata o datetime para string antes de salvar na sessão
            request.session['last_activity'] = now().isoformat().replace('+00:00', 'Z') # Formato ISO 8601 com Z para UTC

        response = self.get_response(request)
        return response