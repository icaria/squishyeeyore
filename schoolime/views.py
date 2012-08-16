# Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
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

def index_view(request):
    if "loggedin" in request.session:
        if request.session["loggedin"]:
            return HttpResponseRedirect("/home")

    return render(request, 'index.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pw = form.cleaned_data['pw']
            
            try:
                user = Student.objects.get(Q(email=email)|Q(user_name=email), Q(password=pw))
                request.session['user'] = user
                request.session['loggedin'] = True
                return HttpResponseRedirect("/home")
            except Student.DoesNotExist:
                form.errors['__all__'] = form.error_class(["The password you entered is incorrect, please try again."])
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form,})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            student = Student(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                              user_name=form.cleaned_data['user_name'], email=form.cleaned_data['email'], 
                              password=form.cleaned_data['password'], is_active=False)
            
            student.save()
            return HttpResponseRedirect("/register-success/")
    else:
        form = RegisterForm()
    
    return render(request, 'registration/registration_form.html', {'form': form,})

def register_success_view(request):
    return render(request, 'registration/registration_complete.html')
    
def logout_view(request):
    try:
        del request.session['user']
        request.session['loggedin'] = False
    except KeyError:
        pass
    return HttpResponseRedirect("/")

@user_login_required
def home_view(request):
    user = request.session.get('user')
    form = HomeForm({'first_name' : user.first_name, 'last_name' : user.last_name})
    return render(request, 'home.html', {'form': form,})

@user_login_required
def profile_view(request):
    pass

    