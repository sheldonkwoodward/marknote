from rest_framework import serializers
from rest_framework.serializers import unicode_to_repr

from marknote.models import Note, Folder


class CurrentUserDefault:
    def __init__(self):
        self.user_id = None

    def __call__(self):
        return self.user_id

    def __repr__(self):
        return unicode_to_repr('%s()' % self.__class__.__name__)

    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id


class NoteSummarySerializer(serializers.ModelSerializer):
    owner_id = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Note
        fields = (
            'pk',
            'title',
            'containerId',
            'created',
            'updated',
            'owner_id',
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
    owner_id = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Folder
        fields = (
            'pk',
            'title',
            'containerId',
            'created',
            'updated',
            'owner_id',
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
