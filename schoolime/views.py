# Create your views here.
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from schoolime.models import *
from schoolime.forms import *

##More than one view can be displayed on one form
def user_login_required(f):
    def wrap(request, *args, **kwargs):
        #this check the session if userid key exist, if not it will redirect to login page
        if 'user' not in request.session.keys():
                return HttpResponseRedirect("login")
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

def main_view(request):
    return render_to_response('index.html', None, context_instance=RequestContext(request))

def login_view(request):
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pw = form.cleaned_data['pw']
            
            try:
                user = Student.objects.get(email=email, password=pw)
                request.session['user'] = user
            except Student.DoesNotExist:
                return HttpResponse("Your username and password didn't match.")
            
            return HttpResponseRedirect('/home') # Redirect after POST
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form,})

@user_login_required
def home_view(request):
    user = request.session['user']   
    return render_to_response('home.html', None, context_instance=RequestContext(request))

def logout_view(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return render_to_response('index.html', None, context_instance=RequestContext(request))


    

    