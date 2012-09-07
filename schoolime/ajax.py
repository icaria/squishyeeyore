import datetime
from django.utils import simplejson
from django.http import HttpResponse
from django.http import HttpResponseServerError
from schoolime.models import *
from schoolime.forms import *

def check_profile(request):
    user = request.session["user"]
    if user.profile:
        response_str = "true"
    else:
        response_str = "false"
        
    return HttpResponse(response_str)

def submit_profile(request):
    now = datetime.date.today()
    user = request.session["user"]
    form = HomeForm(request.POST)
    return HttpResponse(form.errors)
    
    if form.is_valid():
        return HttpResponse("true")
    
    return HttpResponse("false")
    #profile = Profile(rank_id=1, school_id=1, program=, display_picture=None, phone=41, birthday=form.cleaned_data["birthday"], about=form.cleaned_data["about"], last_login=now, date_joined=now)
    #profile.save()
     

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