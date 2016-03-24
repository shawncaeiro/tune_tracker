from django.db import models
import datetime

class Song(models.Model):
    title = models.TextField(default='')
    artist = models.TextField(default='')

    def __str__(self):
        return "%s %s" % (self.title, self.artist)

class Rank(models.Model):
    rank = models.IntegerField(default=101)
    week = models.DateField(default=datetime.date(1980,1,1))
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %d %s" % (self.song.title, self.song.artist, self.rank, str(self.week))



