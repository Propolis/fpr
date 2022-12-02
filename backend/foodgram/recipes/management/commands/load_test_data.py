import csv

from django.core.management.base import BaseCommand # , CommandError
from foodgram.settings import BASE_DIR
from recipes.models import Ingridient, Tag

file_model_dict = {
    'tags.csv': Tag, 
    'ingredients.csv': Ingridient,
}
path = str(BASE_DIR) + ('/../../data/')


class Command(BaseCommand):
    help = 'Загружает тестовые данные в бд'

    def handle(self, *args, **options):
        for file, model in file_model_dict.items():
            model.objects.all().delete()
            with open(f'{path}{file}') as file:
                reader = csv.DictReader(file, delimiter=',')
                for data in reader:
                    model.objects.create(**data)
