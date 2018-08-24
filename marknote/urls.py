from django.conf.urls import url
from marknote import views


urlpatterns = [
    url(r'^note$',
        views.NoteListCreateView.as_view(),
        name='note-list-create'),
    url(r'^note/(?P<pk>\d+)$',
        views.NoteRetrieveUpdateDestroyView.as_view(),
        name='note-retrieve-update-destroy'),
    url(r'^folder$',
        views.FolderListCreateView.as_view(),
        name='folder-list-create'),
    url(r'^folder/(?P<pk>\d+)$',
        views.FolderRetrieveUpdateDestroyView.as_view(),
        name='folder-retrieve-update-destroy'),
]
