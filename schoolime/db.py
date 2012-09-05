import datetime
from django.db.models import Q
from schoolime.models import *

def get_current_term():
    date = datetime.datetime.now()
    if date.month < 5:
        term_letter = 'W'
    elif date.month < 9:
        term_letter = 'S'
    else:
        term_letter = 'F'
    return Term.objects.get(Q(year=date.year), Q(term=term_letter))
    