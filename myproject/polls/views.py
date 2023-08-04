from django.http import HttpResponse, Http404
from django.shortcuts import render

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
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    
    return render(request, "polls/detail.html", {"question" : question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)



def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

