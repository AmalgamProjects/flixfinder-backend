import csv
from django.core.management import BaseCommand
from ff_api.models import Name, Title

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
                    titles = []
                    for title in row[5].split(','):
                        try:
                            titles.append(Title.objects.all(tconst=title))
                        except:
                            pass 
                    
                    name = Name.objects.create(
                        nconst=row[0],
                        primaryName=row[1],
                        birthYear=row[2] if row[2] != '\\N' else None,
                        deathYear=row[3] if row[3] != '\\N' else None,
                        primaryProfession=row[4].split(','),
                    )
                    name.save();
                    name.knownForTitles.set(titles)

                count += 1