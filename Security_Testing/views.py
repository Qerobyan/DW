from django.shortcuts import render
from django.http import  JsonResponse
from DW import settings


def index(request):
    return render(request, "index.html")


def sqlin_jection(request):
    return render(request, "search.html")


def xss(request):
    return render(request, "search2.html")


def set_inactive(request):
    """
    It sets the active_connection variable to False

    :param request: The request object
    :return: A JsonResponse object.
    """
    settings.active_connection = False
    return JsonResponse({"message": 'OK!'})


