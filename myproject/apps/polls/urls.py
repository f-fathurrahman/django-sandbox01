from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("another", views.another, name="another")
]
# what is the purpose of `name` kwarg ?