from django.db import models
from myrep import settings
from .validators import validate_file_extension
# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.user.id, filename)

def tunes_user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'sheets/{0}/{1}'.format(instance.user.id, filename)
 

class Key(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Tune(models.Model):
    name = models.CharField(max_length=100)
    composer = models.CharField(max_length=100, null=True, blank=True)
    key = models.CharField(max_length=15, null=True, blank=True)
    genre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class UserTune(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tune = models.ForeignKey(Tune, on_delete=models.CASCADE)
    notes = models.TextField(max_length=400,null=True,blank=True)
    playonpiano = models.BooleanField(default=False)
    playonjamsession = models.BooleanField(default=False)
    playonstage = models.BooleanField(default=False)
    havesheet = models.BooleanField(default=False)
    sheet = models.FileField(upload_to= tunes_user_directory_path , blank=True, null=True, validators=[validate_file_extension])
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.tune.name

