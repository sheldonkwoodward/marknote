from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from marknote.models import Note, Folder
from marknote.serializers import NoteSerializer, FolderSerializer


class NoteListCreateView(ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = NoteSerializer

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
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
