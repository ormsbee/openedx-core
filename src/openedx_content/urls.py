from django.urls import path

from .rest import rest_api

urlpatterns = [
    path("content/", rest_api.urls),
]
