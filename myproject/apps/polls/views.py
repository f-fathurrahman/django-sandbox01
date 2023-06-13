from django.http import HttpResponse

def index(request):
    print("request = ", request)
    return HttpResponse("Hello from efefer. You're at the polls index.")


def another(request):
    print("request = ", request)
    return HttpResponse("Another views.")
