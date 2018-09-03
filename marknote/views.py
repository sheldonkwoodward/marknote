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
        qs = Note.objects.all().filter(owner=self.request.user.id)
        # general search
        print(self.request.user.id)
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

    def list(self, request, *args, **kwargs):
        response = super(NoteListCreateView, self).list(request, *args, **kwargs)
        response.data = {
            'notes': response.data,
        }
        return response


class NoteRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        return Note.objects.all().filter(owner=self.request.user.id)


class FolderListCreateView(ListCreateAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.FolderSummarySerializer

    def get_queryset(self):
        qs = Folder.objects.all().filter(owner=self.request.user.id)
        query = self.request.GET.get('search')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        query = self.request.GET.get('title')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs

    def list(self, request, *args, **kwargs):
        response = super(FolderListCreateView, self).list(request, *args, **kwargs)
        response.data = {
            'folders': response.data,
        }
        return response


class FolderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.FolderSerializer

    def get_queryset(self):
        return Folder.objects.all().filter(owner=self.request.user.id)
