import csv
from django.core.management import BaseCommand
from ff_api.models import Rating

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
                  rating = Rating.objects.create(
                  tconst=row[0],
                  averageRating=row[1],
                  numVotes=row[2]
                )
            count += 1