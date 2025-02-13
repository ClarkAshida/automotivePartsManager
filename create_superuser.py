import os
import django
from django.contrib.auth import get_user_model

# Configurar o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

User = get_user_model()

# Pegando variáveis de ambiente
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@hubbi.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "Admin!123")

# Criando o superusuário apenas se ele não existir
if not User.objects.filter(username=username).exists():
    print(f"🔹 Criando superusuário {username}")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superusuário criado com sucesso!")
else:
    print("✅ Superusuário já existe. Nenhuma ação necessária.")
