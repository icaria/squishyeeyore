from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import simplejson
from django.http import HttpResponse
from django.db.models import Q
from schoolime.models import *
from schoolime.forms import *

def check_profile(request):
    email = request.session["schoolime_user"]
    user = Student.objects.get(email=email)
    if user.has_profile():
        response_str = "true"
    else:
        response_str = "false"

    return HttpResponse(response_str)

def submit_profile(request):
    email = request.session["schoolime_user"]
    user = Student.objects.get(email=email)

    school = request.POST.get("school")
    concentration = request.POST.get("concentration")
    phone = request.POST.get("phone")
    birthday = request.POST.get("birthday")
    birthday_array = birthday.split("-")
    birthday_date = datetime.date(year=int(birthday_array[0]), month=int(birthday_array[1]), day=int(birthday_array[2]))
    about = request.POST.get("about")
#
#    try:
#
#        drive = Drive(size=1024)
#        drive.save()
#
#        #create concentration if it does not exist
#        conc, isCreated = Concentration.objects.get_or_create(school_id=school, concentration=concentration)
#
#        profile = Profile(rank_id=1, school_id=school, drive_id=drive.pk, concentration_id=conc.pk, average=0.0, display_picture=None, phone=phone, birthday=birthday_date, about=about)
#        profile.save()
#
#        student = Student.objects.get(id=user.id)
#        student.profile_id = profile.pk
#        student.save()
#
#        request.session["schoolime_user"] = student
#        return HttpResponse("true")
#    except:
#        return HttpResponse("false")

def send_verification_email(request, student):
    # temporary link goes to localhost
    path = request.get_host()
    link, subject, from_email, to = "http://" + path + "/activate/" + student.verification_key, "Activate Schoolime Account", "registration@schoolime.com", student.email
    html_content = render_to_string('registration/activation_email.html', {'first_name':student.first_name, 'link':link})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponse("true")

def concentration_lookup(request):
#    concentrations = Concentration.objects.filter(Q(concentration__istartswith=request.REQUEST['term']), Q(school_id=int(request.REQUEST['school_id'])))
    results = []
#    for concentration in concentrations:
#        concentration_dict = {'id':concentration.id, 'label':concentration.concentration, 'value':concentration.concentration}
#        results.append(concentration_dict)
#    return HttpResponse(simplejson.dumps(results),mimetype='application/json')

def check_registration(request):
    if "email" in request.GET:
        email = request.GET.get("email")
        if Student.objects.filter(email__exact=email):
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