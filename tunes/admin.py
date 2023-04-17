from django.contrib import admin
from .models import Tune, UserTune, Genre, UserTuneList

# Register your models here.

admin.site.register(Tune)
admin.site.register(UserTune)
admin.site.register(Genre)
admin.site.register(UserTuneList)
