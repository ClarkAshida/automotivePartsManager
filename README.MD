# Sistema de Consulta de Peças Automotivas

Este repositório contém o backend do Sistema de Consulta de Peças Automotivas para o desafio técnico da Hubbi. Siga as instruções abaixo para instalar e configurar o ambiente de desenvolvimento localmente.

## Instalação

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

### 5. Configurar o Banco de Dados

Prepare o banco de dados executando as migrações:

#### Criar as migrações (se necessário):

```bash
python manage.py makemigrations
```

#### Aplicar as migrações:

```bash
python manage.py migrate
```

### 6. Criar um Superusuário

Para acessar o painel administrativo do Django, você precisa criar um superusuário:

```bash
python manage.py createsuperuser
```

Siga as instruções no terminal para definir o nome de usuário, e-mail e senha.

### 7. Rodar o Servidor de Desenvolvimento

Agora, você pode rodar o servidor de desenvolvimento para testar a aplicação localmente:

```bash
python manage.py runserver
```

A aplicação estará disponível em http://127.0.0.1:8000/ por padrão.

### 7.1 Rodando o Servidor de Desenvolvimento com o Docker

O docker te permite acessar o banco de dados do projeto de forma fácil e sem ter que instalar o Postgresql. Basta aplicar o comando:

```bash
sudo docker-compose build
```

```bash
sudo docker-compose up
```

e em outro terminal aplicar o comando de inicialização do servidor:

```bash
python manage.py runserver
```
