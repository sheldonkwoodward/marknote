from rest_framework.serializers import ModelSerializer

from marknote.models import Note, Folder


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = (
            'id',
            'title',
            'content',
            'containerId',
            'created',
            'updated',
        )


class FolderSerializer(ModelSerializer):
    class Meta:
        model = Folder
        fields = (
            'id',
            'title',
            'containerId',
            'created',
            'updated',
        )
