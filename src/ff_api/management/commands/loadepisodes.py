import csv
from django.core.management import BaseCommand
from ff_api.models import Episode

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
                    try:
                        title = Title.objects.get(tconst=row[0])
                    except:
                        continue
                    episode = Episode.objects.create(
                        tconst=title,
                        parentTconst=row[1],
                        seasonNumber=row[2],
                        episodeNumber=row[3]
                    )
            count += 1