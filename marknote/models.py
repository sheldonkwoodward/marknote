from django.db import models


class Base(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    title = models.CharField(max_length=30)
    containerId = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['title', '-updated']


class Note(Base):
    content = models.TextField(null=True)

    class Meta:
        db_table = 'marknote_notes'


class Folder(Base):
    class Meta:
        db_table = 'marknote_folders'
