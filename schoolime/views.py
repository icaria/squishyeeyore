# Create your views here.
import random, string
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import make_password, check_password
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
            user = Student.objects.get(Q(email=email)|Q(user_name=email))
                  
            if check_password(pw, user.password):
                request.session['user'] = user
                request.session['loggedin'] = True
                return HttpResponseRedirect("/home")
            else:
                form.errors['__all__'] = form.error_class(["The password you entered is incorrect, please try again."])
                
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form,})
    
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            student = Student(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                              profile=None, user_name=form.cleaned_data['user_name'], email=form.cleaned_data['email'], 
                              password=make_password(form.cleaned_data['password']), is_active=True, is_verified=False)
            
            student.save()
            
            # send verification email
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for n in range(20));
            verification = VerificationKey(student=student, key=key)
            verification.save()
            
            # temporary link goes to localhost
            link, subject, from_email, to = "http://127.0.0.1:8000/activate/" + key, "Activate Schoolime Account", "registration@schoolime.com", student.email
            html_content = render_to_string('registration/activation_email.html', {'first_name':student.first_name, 'link':link})
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            return HttpResponseRedirect("/register-success/")
    else:
        form = RegisterForm()
    
    return render(request, 'registration/registration_form.html', {'form': form,})

def register_success_view(request):
    return render(request, 'registration/registration_complete.html')

def activate_user_view(request, key):
    
    try:
        #First, the code tries to look up the user based on the activation key
        user = VerificationKey.objects.get(key=key)
        student = Student.objects.get(id=user.student_id)
        
        #If found, and the user is not active, the user's account is activated.
        if student.is_verified == False:
            student.is_verified = True
            student.save()
            
            VerificationKey.objects.get(key=key).delete()
        #Else, if the user is already active, an error page is passed
        else:
            raise Http404(u'Account already activated')
    #If no user is found with the activation key, an error page is passed
    except VerificationKey.DoesNotExist:
        raise Http404(u'No activation key found')
 
    return render(request, 'registration/activate.html')
    
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

    