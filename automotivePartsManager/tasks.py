import csv
import io
from celery import shared_task
from django.core.cache import cache
from .models import Part

@shared_task
def process_csv(file_data):
    """
    Tarefa assíncrona que processa um arquivo CSV e adiciona peças ao banco de dados.
    """
    decoded_file = file_data.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded_file))

    parts = []
    for row in reader:
        part = Part(
            part_number=row['part_number'],
            name=row['name'],
            details=row['details'],
            price=float(row['price']),
            quantity=int(row['quantity'])
        )
        parts.append(part)

    Part.objects.bulk_create(parts)

    # Limpar cache após inserção
    cache.delete('parts_list')
