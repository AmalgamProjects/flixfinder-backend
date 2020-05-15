import csv
import pprint
import time

from django.core.management import BaseCommand

from ...models import Title, Genre


class Command(BaseCommand):
    help = 'Load files into the db'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, required=True)
        parser.add_argument('--rowstart', type=int, default=0)
        parser.add_argument('--rowstop', type=int, default=6802944)

    # noinspection PyBroadException
    def handle(self, *args, **kwargs):
        ignore_rows_before = kwargs['rowstart']
        ignore_rows_after = kwargs['rowstop']
        number_rows = ignore_rows_after - ignore_rows_before
        start_time = int(time.time())
        last_time = start_time
        last_count = 0
        last_dbcount = 0
        count = 0
        dbcount = 0
        path = kwargs['path']
        pprint.pprint("reading " + path)
        with open(path, 'rt') as f:
            reader = csv.reader(f, delimiter="\t", quotechar='"')
            for row in reader:
                count += 1
                if count <= ignore_rows_before:
                    continue
                if count >= ignore_rows_after:
                    break
                now = int(time.time())
                if last_time < now:
                    eta = int((number_rows - (count - ignore_rows_before)) / (
                            (count - ignore_rows_before) / (now - start_time)))
                    if eta > 3600:
                        eta = str(int(eta / 3600)) + ' hours'
                    elif eta > 60:
                        eta = str(int(eta / 60)) + ' minutes'
                    pprint.pprint(
                        'second: %s rows (count=%s) .. %s db (count=%s) .. eta %s' % (
                            count - last_count, count,
                            dbcount - last_dbcount, dbcount,
                            eta
                        )
                    )
                    last_time = now
                    last_count = count
                    last_dbcount = dbcount
                titleType = row[1]
                # movie,short,titleType,tvEpisode,tvMiniSeries,tvMovie,tvSeries,tvShort,tvSpecial,video,videoGame
                if titleType not in ['movie', 'tvMovie', 'tvSeries', 'tvMiniSeries']:
                    continue
                release = 0
                try:
                    release = int(row[5])
                    if titleType != 'movie' and release < 2000:
                        continue
                    if titleType == 'movie' and release < 1980:
                        continue
                except Exception as e:
                    pass
                try:
                    release = int(row[6])
                    if titleType != 'movie' and release < 2000:
                        continue
                    if titleType == 'movie' and release < 1980:
                        continue
                except Exception as e:
                    pass
                try:
                    dbcount += 1
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

                    genres = []
                    for genre in row[8].split(','):
                        try:
                            result = Genre.objects.filter(name=genre).first()
                        except Exception:
                            result = Genre.objects.create(name=genre)
                        genres.append(result)
                    title.genres.set(genres)

                    pprint.pprint("%s - Created   %12s %8s %s (%s)" % (count, row[0], row[1], row[2], release))

                except Exception as e:
                    if 'Duplicate entry' not in str(e):
                        pprint.pprint("%s - Exception %12s %8s %s (%s)" % (count, row[0], row[1], row[2], release))
                        pprint.pprint(str(e))
                    pass
