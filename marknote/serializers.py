from rest_framework.serializers import ModelSerializer

from marknote.models import Note, Folder


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = (
            'pk',
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
            'pk',
            'title',
            'containerId',
            'created',
            'updated',
        )
