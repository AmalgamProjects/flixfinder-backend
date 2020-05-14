import csv
from django.core.management import BaseCommand
from ff_api.models import Title, Genre

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
                    release = int(row[6])
                    running = int(row[7])
                except:
                    continue
                if count > 1 and release > 1990 and running > 15:
                    genres = []
                    for genre in row[8].split(','):
                        try:
                            result = Genre.objects.get(name=genre)
                        except:
                            result = Genre.objects.create(name=genre)
                        genres.append(result)
                    
                    title = Title.objects.create(
                        tconst=row[0],
                        titleType=row[1],
                        primaryTitle=row[2],
                        originalTitle=row[3],
                        isAdult=row[4],
                        startYear=row[5],
                        endYear=row[6],
                        runtimeMinutes=row[7]
                    )
                    
                    title.save()
                    title.genres.set(genres)
                count += 1