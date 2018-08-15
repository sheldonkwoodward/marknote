from django.db import models


class Base(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    title = models.CharField(max_length=30)
    containerId = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True


class Note(Base):
    content = models.TextField(null=True)
    timestamp = models.IntegerField()


class Folder(Base):
    pass
