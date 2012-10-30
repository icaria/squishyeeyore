# Create your views here.
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect
from django.db.models import Q
from schoolime.forms import *
from schoolime.ajax import *
from schoolime.decorators import *
from schoolime.models import *

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
                if user.login(pw):
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
            student = Student.create(form.cleaned_data['first_name'],
                                     form.cleaned_data['last_name'],
                                     form.cleaned_data['email'],
                                     form.cleaned_data['password'])

            request.session['schoolime_user'] = student.email
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

        student = Student.objects.get(verification_key=key)

        #If found, and the user is not active, the user's account is activated.
        if not student.has_verified():
            student.activate_student()
            student.save()

            if "schoolime_loggedin" in request.session:
                if request.session["schoolime_loggedin"]:
                    request.session["schoolime_user"] = student

        #Else, if the user is already active, an error page is passed
        else:
            raise Http404(u'Account already activated')
    #If no user is found with the activation key, an error page is passed
    except Student.DoesNotExist:
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

    curr_term = Term.get_current_term()
    classes = Student.get_current_courses(user.id, curr_term.id)

    return render(request, 'home.html', {'form': form, 'classes': classes})

@user_login_required
def profile_view(request, user):
    user = Student.objects.get(user_name=user)
    form = ProfileForm({'first_name' : user.first_name, 'last_name' : user.last_name})


    return render(request, 'profile.html', {'form': form,})


