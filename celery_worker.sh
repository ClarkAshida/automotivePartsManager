#!/bin/sh

echo "Iniciando o Celery..."
celery -A setup worker --loglevel=info
