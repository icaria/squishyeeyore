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
    
    term, isCreated = Term.objects.get_or_create(year=date.year, term=term_letter)
    return term
