from django.contrib import admin
from .models import Tune, UserTune, Key, Genre

# Register your models here.

admin.site.register(Tune)
admin.site.register(UserTune)
admin.site.register(Key),
admin.site.register(Genre)