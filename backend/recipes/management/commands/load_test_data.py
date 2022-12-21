import csv

from django.core.management.base import BaseCommand
from progress.bar import Bar

from foodgram.settings import BASE_DIR
from recipes.models import Ingredient, Tag

file_model_dict = {
    'tags.csv': Tag,
    'ingredients.csv': Ingredient,
}
path = str(BASE_DIR) + ('/../../data/')


class Command(BaseCommand):
    help = 'Загружает тестовые данные в бд'

    def handle(self, *args, **options):
        for file_path, model in file_model_dict.items():
            with open(f'{path}{file_path}') as file:
                rows = len(file.readlines()) - 1
                file.close()

            with open(f'{path}{file_path}') as file:
                countdown = Bar(
                    f'Creating data from {file_path} > ',
                    max=rows
                )
                reader = csv.DictReader(file, delimiter=',')
                for data in reader:
                    model.objects.create(**data)
                    countdown.next()
                countdown.finish()
