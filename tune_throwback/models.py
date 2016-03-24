from django.db import models
import datetime

class SongRank(models.Model):
    song = models.TextField(default='')
    artist = models.TextField(default='')
    rank = models.IntegerField(default=101)
    week = models.DateField(default=datetime.date(1980,1,1))



