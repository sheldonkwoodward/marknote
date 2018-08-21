from django.db.models import Q
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from marknote import serializers
from marknote.models import Note, Folder


class NoteListCreateView(ListCreateAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.NoteSummarySerializer

    def get_queryset(self):
        qs = Note.objects.all()
        # general search
        query = self.request.GET.get('search')
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        # title search
        query = self.request.GET.get('title')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        # content search
        query = self.request.GET.get('content')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs


class NoteRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.NoteSerializer
    queryset = Note.objects.all()


class FolderListCreateView(ListCreateAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.FolderSummarySerializer

    def get_queryset(self):
        qs = Folder.objects.all()
        query = self.request.GET.get('search')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        query = self.request.GET.get('title')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs


class FolderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.FolderSerializer
    queryset = Folder.objects.all()
