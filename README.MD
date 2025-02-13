# Sistema de Consulta de Peças Automotivas

Bem-vindo ao repositório do Sistema de Consulta de Peças Automotivas! Este projeto foi desenvolvido como parte do desafio técnico da Hubbi e tem como objetivo facilitar a busca e gestão de peças automotivas. 

## Instalação

Siga as instruções abaixo para instalar e configurar o ambiente de desenvolvimento localmente.

### 1. Clonar o Repositório

Primeiro, clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/ClarkAshida/automotivePartsManager.git
cd automotivePartsManager
```

### 2. Criar um Ambiente Virtual

Crie um ambiente virtual Python para isolar as dependências do projeto de acordo com o seu sistema operacional:

#### Windows:
```bash
python -m venv venv
```

#### Mac e Linux:
```bash
python3 -m venv venv
```

### 3. Ativar o Ambiente Virtual
Ative o ambiente virtual com o comando apropriado para o seu sistema operacional:

#### Windows ( Pelo prompt de comand cmd):
```bash
venv\Scripts\activate.bat
```
### pelo Windows (PowerShell)
```bash
.\venv\Scripts\Activate.ps1
```

#### Mac e Linux:
```bash
source venv/bin/activate
```

### 4. Instalar as Dependências

Com o ambiente virtual ativado, instale todas as dependências necessárias para o projeto:

```bash
pip install -r requirements.txt
```

### 5. Configurar o projeto (Sem Docker).

Siga as instruções abaixo para configurar o projeto sem o Docker.

### Observações:

Para configurar o projeto sem o uso de Docker, é necessário ter instalado na sua máquinas as dependências abaixo:

- **Redis**: Utilizado como _Broker_ para o Celery, permitindo a execução de tarefas assíncronas.
- **PostgreSQL**: Banco de dados relacional utilizado para armazenar as informações do sistema.
- **Python**: Interpretador de código necessário para executar o projeto e suas dependências.

### Configurar o Banco de Dados (PostgreSQL)

O projeto utiliza PostgreSQL como banco de dados. Certifique-se de que ele esteja instalado e configure as variáveis de ambiente para conexão. Segue abaixo um exemplo de .env:

```bash
# Configurações do Banco de Dados
DB_NAME=NOME_BANCO_DE_DADOS
DB_USER=NOME_USUARIO
DB_PASSWORD=SENHA
DB_HOST=localhost
DB_PORT=5432

# Configurações de segurança do Django
DJANGO_SECRET_KEY='SEU_SEGREDO'

# URL do Servidor Redis
CELERY_BROKER_URL=redis://redis:6379/0

# Credenciais para o Django Admin
DJANGO_SUPERUSER_USERNAME=USUARIO_ADMIN
DJANGO_SUPERUSER_EMAIL=EMAIL_ADMIN
DJANGO_SUPERUSER_PASSWORD=SENHA_ADMIN
```

adicione as configurações dentro de um arquivo .env na raíz do projeto.

#### Criar as migrações do Banco de Dados

Após configurar o banco, aplique as migrações para criar as tabelas:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Criar um Superusuário

Para acessar o painel administrativo do Django, você precisa criar um superusuário:

```bash
python manage.py createsuperuser
```

Siga as instruções no terminal para definir o nome de usuário, e-mail e senha.

### Iniciar o Servidor de Desenvolvimento

Agora, você pode rodar o servidor de desenvolvimento para testar a aplicação localmente:

```bash
python manage.py runserver
```

A aplicação estará disponível em http://127.0.0.1:8000/ por padrão.

#### Iniciar o Servidor Redis

O Redis é utilizado como broker para o Celery. Certifique-se de que ele está instalado e execute:

```bash
redis-server
```

#### Iniciar o Celery Worker

O celery permite a execução de comandos de forma assíncrona, possibilitando o cadastro de peças automotivas através do upload de arquivos CSV.

```bash
celery -A setup worker --loglevel=info
```

### Configuração finalizada

Dessa forma, o projeto estará devidamente configurado e pronto para ser executado.

### 6. Configuração do projeto (Com Docker).

O docker te permite configurar o projeto de forma fácil e sem ter que instalar as dependências necessárias na sua máquina. É importante ressaltar que você precisa ter o Docker instalado localmente para rodar os comandos abaixo:

### Alterar a variável de ambiente HOST

A variável de ambiente definida por _db_ permite acessar o banco de dados através de uma _imagem_ do Postgresql.

```bash
DB_HOST=db
```

Talvez seja necessário reiniciar o VSCode em caso de conflito ou erro na leitura das variáveis.

### Executar o arquivo Docker Compose

O arquivo Docker Compose contém todos os comandos necessários para inicializar a aplicação, construindo _containers_ do servidor web Django, Banco de Dados Postgresql, servidor Redis e Celery.

```bash
docker-compose up --build -d
```

Você pode verificar o estado de criação dos containers com o comando abaixo:

```bash
docker ps
```

### Acessar o banco de dados com o usuário admin padrão

Ao inicializar o projeto com o Docker, um usuário admin padrão é criado com as credenciais abaixo, sendo possível autenticar os end points do projeto através do token JWT gerado na autenticação.

```bash
{
    "email":"admin@hubbi.com",
    "password":"Admin!123"
}
```

### 7. Inicializar a rotina de testes

Executar a rotina de testes garante que todas as funcionalidades do sistema estão funcionando corretamente e que novas alterações não introduziram bugs. Para rodar os testes, utilize o comando abaixo, que executará todos os testes definidos no projeto:

Com docker:

```bash
docker-compose exec web python manage.py test
```

Sem Docker:

```bash
python manage.py test
```

Isso ajudará a manter a integridade e a confiabilidade do sistema.