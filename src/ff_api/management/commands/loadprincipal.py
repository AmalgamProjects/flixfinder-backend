import csv
from django.core.management import BaseCommand
from ff_api.models import Principal, Title, Name

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
                    
                    try:
                        name = Name.objects.get(nconst=row[2])
                    except:
                        continue
                    
                    principal = Principal.objects.create(
                        tconst=title,
                        ordering=row[1],
                        nconst=name,
                        category=row[3],
                        job=row[4],
                        characters=row[5]
                    )
                    principal.save()
                count += 1