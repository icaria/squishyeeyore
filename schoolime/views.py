# Create your views here.
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from schoolime.forms import *

##More than one view can be displayed on one form

@login_required(login_url='login')
def home_page(request):
    #If users are authenticated, direct them to the main page. Otherwise, take
    #them to the login page.
    return render_to_response('home.html', None, context_instance=RequestContext(request))

def main_page(request):
    return render_to_response('index.html', None, context_instance=RequestContext(request))

def logout_page(request):
    #Log users out and re-direct them to the main page.
    logout(request)
    return HttpResponseRedirect('/')

    