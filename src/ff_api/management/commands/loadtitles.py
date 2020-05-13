import csv
from django.core.management import BaseCommand
from ff_api.models import Title

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
                  title = Title.objects.create(
                  tconst=row[0],
                  titleType=row[1],
                  primaryTitle=row[2],
                  originalTitle=row[3],
                  isAdult=row[4],
                  startYear=row[5],
                  endYear=row[6],
                  runtimeMinutes=row[7],
                  genres=row[8]
                )
            count += 1