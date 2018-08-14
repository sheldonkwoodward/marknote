from django.db import models


class Note(models.Model):
    id = models.CharField(primary_key=True)
    title = models.CharField()
    content = models.TextField()
    folderId = models.CharField()
    timestamp = models.IntegerField()


class Folder(models.Model):
    id = models.CharField(primary_key=True)
    title = models.CharField()
    folderId = models.CharField()
