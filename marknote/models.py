from django.db import models


class Base(models.Model):
    title = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['title', '-updated']


class Folder(Base):
    containerId = models.ForeignKey('self', related_name='folders', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'marknote_folders'


class Note(Base):
    containerId = models.ForeignKey(Folder, related_name='notes', on_delete=models.CASCADE, null=True)
    content = models.TextField()

    class Meta:
        db_table = 'marknote_notes'
