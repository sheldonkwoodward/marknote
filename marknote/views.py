from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from marknote.models import Note, Folder
from marknote import serializers


class NoteListCreateView(ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.NoteSummarySerializer

    def get_queryset(self):
        qs = Note.objects.all()
        query = self.request.GET.get('search')
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        return qs


class NoteRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.NoteSerializer
    queryset = Note.objects.all()


class FolderListCreateView(ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.FolderSummarySerializer

    def get_queryset(self):
        qs = Folder.objects.all()
        query = self.request.GET.get('search')
        if query is not None:
            qs = qs.filter(Q(title__icontains=query)).distinct()
        return qs


class FolderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.FolderSerializer
    queryset = Folder.objects.all()
