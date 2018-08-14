from django.conf.urls import url
from marknote import views


urlpatterns = [
    url(r'^note$', views.Note.as_view())
]
