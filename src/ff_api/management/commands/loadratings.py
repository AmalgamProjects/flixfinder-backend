import csv
from django.core.management import BaseCommand
from ff_api.models import Rating, Title

class Command(BaseCommand):
    help = 'Load files into the db'
    
    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        
    def handle(self, *args, **kwargs):
        count = 1
        path = kwargs['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f, delimiter="\t", quotechar='"')
            for row in reader:
                try:
                    title = Title.objects.get(tconst=row[0])
                except:
                    continue
                
                if count > 1:
                    rating = Rating.objects.create(
                        tconst=title,
                        averageRating=row[1],
                        numVotes=row[2]
                    )
                    rating.save()
                count += 1