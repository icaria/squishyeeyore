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
    if "schoolime_user" in request.session:
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
                    request.session['schoolime_user'] = user.email
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

            send_verification_email(request, student)
            return HttpResponseRedirect("/register-success/")
    else:
        form = RegisterForm()

    return render(request, 'registration/registration_form.html', {'form': form,})

def register_success_view(request):
    return render(request, 'registration/registration_complete.html')

def activate_user_view(request, key):
    try:
        student = Student.objects.get(verification_key=key)
        if not student.verified():
            student.activate_student()
            form = ActivateForm({'first_name' : student.first_name, 'last_name' : student.last_name,
                                 'user_name' : student.user_name, 'is_verified' : student.is_verified })

        else:
            raise Http404(u'Account already activated')
    except Student.DoesNotExist:
        raise Http404(u'No activation key found')

    return render(request, 'registration/activate.html', {'form': form,})

def logout_view(request):
    if "schoolime_user" in request.session:
        del request.session['schoolime_user']
    return HttpResponseRedirect("/")

@user_login_required
def home_view(request):
    email = request.session.get('schoolime_user')
    user = Student.objects.select_related(depth=2).get(email=email)
    form = HomeForm({'first_name' : user.first_name, 'last_name' : user.last_name, 'user_name' : user.user_name, 'is_verified' : user.is_verified })

    curr_term = Term.get_current_term()

    classes = user.get_current_courses(curr_term.id)
    return render(request, 'home.html', {'form': form, 'classes': classes})

@user_login_required
def profile_view(request, user):
    email = request.session.get('schoolime_user')
    user = Student.get(email=email)
    form = ProfileForm({'first_name' : user.first_name, 'last_name' : user.last_name, 'user_name' : user.user_name, 'is_verified' : user.is_verified })


    return render(request, 'profile.html', {'form': form,})


