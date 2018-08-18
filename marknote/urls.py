from django.conf.urls import url
from marknote import views


urlpatterns = [
    url(r'^note$', views.NoteListCreateView.as_view()),
    url(r'^note/(?P<pk>\d+)$', views.NoteRetrieveUpdateDestroyView.as_view()),
]
