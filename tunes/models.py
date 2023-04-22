from django.db import models
from django.db.models import Q
from myrep import settings
from .validators import validate_file_extension, validate_file_size
import os
# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.user.id, filename)

def tunes_user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'sheets/{0}/{1}'.format(instance.user.id, filename)
 

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    

class UserTuneListManager(models.Manager):
    def search(self, query):
        lookups = Q(name__icontains=query) | Q(user__username__icontains=query)
        return UserTuneList.objects.filter(lookups)


class UserTuneManager(models.Manager):
    def search(self, query):
        lookups = Q(tune__name__icontains=query) | Q(user__username__icontains=query) | Q(tune__key__icontains=query) | Q(tune__composer__icontains=query) | Q(tune__genre__icontains=query)
        return UserTune.objects.filter(lookups)



class Tune(models.Model):

    KEY_CHOICHES = (
        ('C maj','C maj'), ('G maj','G maj'), ('D maj','D maj'), ('A maj','A maj'), ('E maj','E maj'), ('F maj','F maj'),
        ('B maj','B maj'), ('Cb maj','Cb maj'), ('Gb maj','Gb maj'), ('F# maj','F# maj'), ('Db maj','Db maj'),
        ('C# maj','C# maj'), ('Ab maj','Ab maj'), ('Eb maj','Eb maj'), ('Bb maj','Bb maj')
        
    )
    
    name = models.CharField(max_length=100)
    composer = models.CharField(max_length=100, null=True, blank=True)
    key = models.CharField(max_length=15, null=True, blank=True, choices=KEY_CHOICHES)
    genre = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class UserTune(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tune = models.ForeignKey(Tune, on_delete=models.CASCADE)
    notes = models.TextField(max_length=400,null=True,blank=True)
    lyrics = models.TextField(max_length=10000, null=True, blank=True)
    playonpiano = models.BooleanField(default=False)
    playonjamsession = models.BooleanField(default=False)
    playonstage = models.BooleanField(default=False)
    havesheet = models.BooleanField(default=False)
    sheet = models.FileField(upload_to= tunes_user_directory_path , blank=True, null=True, validators=[validate_file_extension, validate_file_size])
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    public = models.BooleanField(default=False)

    objects = UserTuneManager()

    def __str__(self) -> str:
        return self.tune.name
    
    @property
    def filename(self):
        return os.path.basename(self.sheet.name)


class UserTuneList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    tunes = models.ManyToManyField(UserTune)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    public = models.BooleanField(default=False)

    objects = UserTuneListManager()

    class Meta:
        ordering = ["updated"]

    def __str__(self):
        return self.name
    