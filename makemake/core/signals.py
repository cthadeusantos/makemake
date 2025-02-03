from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
import logging
#from auditlog.context import set_actor

from makemake.core.custom_functions import get_client_ip

# @receiver(user_logged_in)
# def log_user_login(sender, request, user, **kwargs):
#     # Obter o IP do cliente
#     ip = get_client_ip(request)

#     # Configure o ator e defina o IP manualmente
#     with set_actor(user):
#         LogEntry.objects.log_create(
#             instance=user,
#             action=LogEntry.Action.LOGIN,
#             changes={"event": "Login realizado"},
#             actor=user,
#             remote_addr=ip,
#         )

logger = logging.getLogger(__name__)  # Para registro adicional em logs (opcional)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    # Obtém o IP da requisição
    ip = get_client_ip(request)
    
    # Opcional: registre a informação no banco ou em logs
    logger.info(f"Usuário {user.username} logado em {now()} com IP: {ip}")

    # Exemplo de salvar no modelo (veja o próximo passo para criar um modelo)
    if hasattr(user, "userlog"):  # Supondo que um campo OneToOneField ou FK esteja ligado ao usuário
        user.userlog.create(last_login_ip=ip, login_time=now())