# Usa uma imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . .

# Dá permissão de execução ao script do Celery
RUN chmod +x /app/celery_worker.sh

# Instala as dependências do projeto
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expõe a porta padrão do Django
EXPOSE 8000

# Comando de entrada padrão
CMD ["gunicorn", "-b", "0.0.0.0:8000", "setup.wsgi:application"]
