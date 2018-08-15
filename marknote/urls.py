from django.conf.urls import url
from marknote import views


urlpatterns = [
    url(r'^note$', views.NoteView.as_view())
]
