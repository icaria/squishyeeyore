# Create your views here.
import datetime
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from schoolime.forms import *
from schoolime.services.ajax import *
from schoolime.services.db import *
from schoolime.decorators import *

def index_view(request):
    if "schoolime_loggedin" in request.session:
        if request.session["schoolime_loggedin"]:
            return HttpResponseRedirect("/home")

    return render(request, 'index.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pw = form.cleaned_data['pw']
            try:
                user = Student.objects.get(Q(email=email)|Q(user_name=email))
                if check_password(pw, user.password):
                    user.last_login = datetime.datetime.now()
                    user.save()
                    request.session['schoolime_user'] = user
                    request.session['schoolime_loggedin'] = True
                    return HttpResponseRedirect("/home")
                else:
                    form.errors['__all__'] = form.error_class(["The password you entered is incorrect, please try again."])
            except Student.DoesNotExist:
                form.errors['__all__'] = form.error_class(["The user name you entered does not exist, please try again."])
               
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form,})
    
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            now = datetime.datetime.now()
            em = form.cleaned_data['email']
            
            student = Student(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                              profile_id=None, user_name=em[:em.index('@')], email=em, 
                              password=make_password(form.cleaned_data['password']), is_active=True, is_verified=False, last_login=now, date_joined=now)
            
            student.save()
            
            s_name = student.first_name + " " + student.last_name
            student_node = StudentNode.objects.create(student_id=student.pk, student_name=s_name)
            student_node.save()
            
            request.session['schoolime_user'] = student
            send_verification_email(request)
            
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
            
            if "schoolime_loggedin" in request.session:
                if request.session["schoolime_loggedin"]:
                    request.session["schoolime_user"] = student

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
        del request.session['schoolime_user']
        request.session['schoolime_loggedin'] = False
    except KeyError:
        pass
    return HttpResponseRedirect("/")

@user_login_required
def home_view(request):
    user = request.session.get('schoolime_user')
    form = HomeForm({'first_name' : user.first_name, 'last_name' : user.last_name})
    
    return render(request, 'home.html', {'form': form,})

@user_login_required
def profile_view(request, user):
    user = Student.objects.get(user_name=user)
    form = ProfileForm({'first_name' : user.first_name, 'last_name' : user.last_name})
    
    curr_term = get_current_term()
    classes = Transcript.objects.filter(Q(student_id=user.id), Q(offering__term_id=curr_term.id))

    return render(request, 'profile.html', {'form': form,})

    
