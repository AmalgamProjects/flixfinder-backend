"""
https://docs.djangoproject.com/en/2.2/ref/contrib/admin/

"""

from django.contrib import admin

from ..models import *

# favourite
admin.site.register(Favourite)
admin.site.register(FavouriteGenre)

# imdb
admin.site.register(Title)
admin.site.register(Name)
admin.site.register(Crew)
admin.site.register(Episode)
admin.site.register(Principal)
admin.site.register(Rating)
admin.site.register(Genre)

# seen
admin.site.register(Seen)

# watch
admin.site.register(Watch)
