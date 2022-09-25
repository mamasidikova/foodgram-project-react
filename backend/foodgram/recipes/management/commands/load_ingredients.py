import csv
import os

from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient

NEW_BASE_DIR = os.path.split(os.path.split(BASE_DIR)[0])[0]


class Command(BaseCommand):
    help = 'Import ingredients from json'

    def handle(self, *args, **options):
        with open(NEW_BASE_DIR + r"/data/ingredients.csv", 'r',
                  encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
                name, unit = row
                Ingredient.objects.get_or_create(name=name, unit=unit)
