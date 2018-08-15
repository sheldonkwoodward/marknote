from django.db import models


class Note(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    title = models.CharField(max_length=30)
    content = models.TextField()
    folderId = models.CharField(max_length=36)
    timestamp = models.IntegerField()


class Folder(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    title = models.CharField(max_length=30)
    folderId = models.CharField(max_length=36)
