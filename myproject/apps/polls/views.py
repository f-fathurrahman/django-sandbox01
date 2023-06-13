from django.http import HttpResponse

def index(request):
    print(request)
    return HttpResponse("Hello from efefer. You're at the polls index.")

