from django.utils import simplejson
from django.http import HttpResponse
from django.http import HttpResponseServerError
from schoolime.models import *

def check_registration(request):
    if "email" in request.GET:
        email = request.GET.get("email")
        if Student.objects.filter(email__iexact=email):
            response_str = "false"
        else:
            response_str = "true"
    elif "user_name" in request.GET:
        user_name = request.GET.get("user_name")
        if Student.objects.filter(user_name__iexact=user_name):
            response_str = "false"
        else:
            response_str = "true"
    return HttpResponse(response_str)