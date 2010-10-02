from django.db import models

# Create your models here.
class Playlist(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateTimeField('date created')
    ip = models.IPAddressField()
    request = models.CharField(max_length=32)

    def __unicode__(self):
        return self.title

class Video(models.Model):
    playlist = models.ForeignKey(Playlist)
    youtube_id = models.CharField(max_length=60)
    title = models.CharField(max_length=150)
    youtube_query = models.CharField(max_length=200)
    idx = models.SmallIntegerField()

    def __unicode__(self):
        return self.title
