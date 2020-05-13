import csv
from django.core.management import BaseCommand
from ff_api.models import Name

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
                  name = Name.objects.create(
                  nconst=row[0],
                  primaryName=row[1],
                  birthYear=row[2],
                  deathYear=row[3],
                  primaryProfession=row[4],
                  knownForTitles=row[5],
                )
            count += 1