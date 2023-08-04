from django.urls import path

from . import views

urlpatterns = [
    #
    # example: /polls/
    path("", views.index, name="index"),
    #
    # example: /polls/2/
    path("<int:question_id>/", views.detail, name="detail"),
    #
    # example: /polls/2/results/
    path("<int:question_id>/results/", views.results, name="results"),
    #
    # example: /polls/2/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]