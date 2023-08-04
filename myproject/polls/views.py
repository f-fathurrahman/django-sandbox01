from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Question


def index(request):

    # Get the objects that we want to pass, i.e. the Question's
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # Create context dict, to be passed to template
    context = {
        "latest_question_list": latest_question_list,
    }

    # Return the response with template, also need to pass request argument
    return render(request, "polls/index.html", context)



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question" : question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)



def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

