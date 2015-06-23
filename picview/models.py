from django.db import models

class User(models.Model):
    userName = models.CharField(max_length=20)

class Picture(models.Model):
    owner = models.ForeignKey('User')
    location = models.CharField(max_length=250)
    timestamp = models.DateTimeField(db_index=True)
    userLikes = models.IntegerField(db_index=True, default=0)

class PictureTag(models.Model):
    title = models.CharField(max_length=30)
    tagLinks = models.ManyToManyField(Picture, db_index=True)