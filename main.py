import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar o Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "makemake.settings")
django.setup()

# Caminho do banco de dados SQLite
db_path = "db.sqlite3"

def run():
    # Se o banco de dados não existir, criar as tabelas
    if not os.path.exists(db_path):
        print("🔧 Banco de dados não encontrado. Criando tabelas...")
        execute_from_command_line(["manage.py", "makemigrations"])
        execute_from_command_line(["manage.py", "migrate"])

        # Criar o superusuário com senha fixa
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            print("🔑 Criando superusuário...")
            User.objects.create_superuser(username="admin", password="admin", email="admin@example.com")
            print("✅ Superusuário criado com sucesso! (admin/admin)")

    # Iniciar o servidor
    print("🚀 Iniciando o servidor...")
    execute_from_command_line(["manage.py", "runserver"])

if __name__ == "__main__":
    run()
