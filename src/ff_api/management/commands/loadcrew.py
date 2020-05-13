import csv
from django.core.management import BaseCommand
from ff_api.models import Crew, Name, Title

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
                if count > 1:
                    try:
                        title = Title.objects.get(tconst=row[0])
                    except:
                        continue
                    
                    directors = []
                    writers = []
                    for director in row[1].split(','):
                        try:
                            result = Name.objects.get(nconst=director)
                            directors.append(result)
                        except:
                            pass
                    
                    for writer in row[2].split(','):
                        try:
                            result = Name.objects.get(nconst=writer)
                            writers.append(result)
                        except:
                            pass
                        
                    crew = Crew.objects.create(tconst=title)
                    crew.save()
                    crew.directors.set(directors)
                    crew.writers.set(writers)
                count += 1