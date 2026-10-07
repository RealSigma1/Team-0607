from django.urls import path

from fleet.views import catalog, health


urlpatterns = [
    path("", catalog, name="catalog"),
    path("health/", health, name="health"),
]
