import csv
from django.core.management import BaseCommand
from ff_api.models import Principal

class Command(BaseCommand):
    help = 'Load files into the db'
    
    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        
    def handle(self, *args, **kwargs):
        count = 1
        path = kwargs['path']
        with open(path, 'rt') as f:
            if count > 1:
                reader = csv.reader(f, delimiter="\t", quotechar='"')
                for row in reader:
                  principal = Principal.objects.create(
                  tconst=row[0],
                  ordering=row[1],
                  nconst=row[2],
                  category=row[3],
                  job=row[4],
                  characters=row[5]
                )
            count += 1