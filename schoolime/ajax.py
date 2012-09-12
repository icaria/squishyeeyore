from django.utils import simplejson
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.db.models import Q
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
    user = request.session["user"]
        
    school = request.POST.get("school")
    concentration = request.POST.get("concentration")
    phone = request.POST.get("phone")
    birthday = request.POST.get("birthday")
    birthday_array = birthday.split("-")
    birthday_date = datetime.date(year=int(birthday_array[0]), month=int(birthday_array[1]), day=int(birthday_array[2]))
    about = request.POST.get("about")

    try:

        drive = Drive()
        drive.save()
        
        #create concentration if it does not exist
        conc, isCreated = Concentration.objects.get_or_create(school_id=school, concentration=concentration)
        
        profile = Profile(rank_id=1, school_id=school, drive_id=drive.pk, concentration_id=conc.pk, average=0.0, display_picture=None, phone=phone, birthday=birthday_date, about=about)
        profile.save()
        
        student = Student.objects.get(id=user.id)
        student.profile_id = profile.pk
        student.save()
        request.session["user"] = student
        return HttpResponse("true")
    except:
        return HttpResponse("false")

def concentration_lookup(request):
    concentrations = Concentration.objects.filter(Q(concentration__istartswith=request.REQUEST['term']), Q(school_id=int(request.REQUEST['school_id'])))
    results = []
    for concentration in concentrations:
        concentration_dict = {'id':concentration.id, 'label':concentration.concentration, 'value':concentration.concentration}
        results.append(concentration_dict)
    return HttpResponse(simplejson.dumps(results),mimetype='application/json')

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