from rest_framework import serializers

from marknote.models import Note, Folder


class NoteSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            'pk',
            'title',
            'containerId',
            'created',
            'updated',
        )


class NoteSerializer(serializers.ModelSerializer):
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


class FolderSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = (
            'pk',
            'title',
            'containerId',
            'created',
            'updated',
        )


class FolderSerializer(serializers.ModelSerializer):
    notes = NoteSummarySerializer(many=True, read_only=True)
    folders = FolderSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = (
            'pk',
            'title',
            'containerId',
            'notes',
            'folders',
            'created',
            'updated',
        )
