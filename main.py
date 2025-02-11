import os
import sys
import django
from django.core.management import execute_from_command_line

# Definir o nome do diretório do projeto (substitua por seu projeto real)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ENVIROMENT_DIR = PROJECT_DIR + '/makemake/'
ENV_FILE = os.path.join(ENVIROMENT_DIR, ".env")
DB_FILE = os.path.join(PROJECT_DIR, "db.sqlite3")
print(PROJECT_DIR)
print(ENVIROMENT_DIR)
print(ENV_FILE)
print(DB_FILE)
exit()

def create_env_file():
    """Cria o arquivo .env se não existir."""
    if not os.path.exists(ENV_FILE):
        print("🔧 Arquivo .env não encontrado. Criando...")
        with open(ENV_FILE, "w") as env_file:
            env_file.write("""SECRET_KEY=7)p5$jx7g$8jpv-xr6_j^g1vv9fepvw7esrve2wce+o-52_u-5
DEBUG=False
ALLOWED_HOSTS=*
""")
        print("✅ Arquivo .env criado com sucesso!")

def setup_django():
    """Configura e inicia o Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seu_projeto.settings")
    django.setup()

def initialize_database():
    """Verifica e inicializa o banco de dados se necessário."""
    if not os.path.exists(DB_FILE):
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

def run_server():
    """Inicia o servidor Django."""
    print("🚀 Iniciando o servidor...")
    execute_from_command_line(["manage.py", "runserver"])

if __name__ == "__main__":
    create_env_file()
    setup_django()
    initialize_database()
    run_server()
