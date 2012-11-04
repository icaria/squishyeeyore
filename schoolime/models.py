import datetime, random, string
from django.contrib.auth.hashers import make_password, check_password
from neo4django import Outgoing
from neo4django.db import models
from neo4django.db.models.query import Query, OPERATORS,\
    return_filter_from_conditions, Condition

today = datetime.date.today()
YEAR = range(today.year, today.year-100, -1)

#class UserGroupRelationship(relationships.Relationship):
#    joined = models.DateProperty()

#========================================
# Root
#========================================

class Entity(models.NodeModel):
    def __unicode__(self):
        return "Entity"

class Drive(models.NodeModel):
    student = models.Relationship('Student', rel_type=Outgoing.DRIVE_STUDENT, related_single=True, related_name='drive')
    size = models.IntegerProperty(max_length=20)
    def __unicode__(self):
        return "Drive"

class SchoolType(models.NodeModel):
    schools = models.Relationship('School', rel_type=Outgoing.SCHOOLS, related_single=False, related_name='schools')
    type = models.StringProperty(max_length=60)
    def __unicode__(self):
        return self.type

class GroupType(models.NodeModel):
    groups = models.Relationship('Group', rel_type=Outgoing.GROUPS, related_single=False, related_name='groups')
    type = models.StringProperty(max_length=20)
    def __unicode__(self):
        return self.type

class ContentType(models.NodeModel):
    type = models.StringProperty(max_length=64)
    def __unicode__(self):
        return self.type

class Rank(models.NodeModel):
    number_stars = models.IntegerProperty()
    title = models.StringProperty(max_length=30)
    def __unicode__(self):
        return self.title

class Achievement(models.NodeModel):
    name = models.StringProperty(max_lengnth=32)
    description = models.StringProperty(max_length=255)
    requirement = models.StringProperty(max_length=64)
    def __unicode__(self):
        return self.name

class Term(models.NodeModel):
    term_letter = models.StringProperty()
    year = models.IntegerProperty()

    @classmethod
    def get_current_term(cls):
        date = datetime.datetime.now()
        if date.month < 5:
            term_letter = 'W'
        elif date.month < 9:
            term_letter = 'S'
        else:
            term_letter = 'F'
        (term, isCreated) = cls.objects.get_or_create(year=date.year, term_letter=term_letter)
        return term

class Country(models.NodeModel):
    provinces_states = models.Relationship('ProvinceState', rel_type=Outgoing.PROVINCES_STATES, related_single=False, related_name='provinces_states')
    country = models.StringProperty(max_length=30)
    def __unicode__(self):
        return self.country

class ProvinceState(models.NodeModel):
    country = models.Relationship('Country', rel_type=Outgoing.PROVINCE_STATE_COUNTRY, related_single=True, related_name='country')
    province_state = models.StringProperty(max_length=30)
    def __unicode__(self):
        return u"%s_%s" % (self.country, self.province_state)

class Address(models.NodeModel):
    country = models.Relationship('Country', rel_type=Outgoing.ADDRESS_COUNTRY, related_single=True, related_name='country')
    province_state = models.Relationship('ProvinceState', rel_type=Outgoing.ADDRESS_PROVINCE_STATE, related_single=True, related_name='province_state')
    street_address = models.StringProperty(max_length=60)
    city = models.StringProperty(max_length=30)
    def __unicode__(self):
        return u"%s, %s, %s %s" % (self.street_address, self.city, self.province_state, self.country)

#========================================
# Entities
#========================================

class Person(Entity):
    school = models.Relationship('School', rel_type=Outgoing.PROFESSOR_SCHOOL, related_single=False, related_name="school")
    first_name = models.StringProperty(max_length=30)
    last_name = models.StringProperty(max_length=30)
    email = models.EmailProperty(max_length=75, indexed=True)
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

class Content(Entity):
    actor = models.Relationship('Student', rel_type=Outgoing.SOURCE, related_single=True, related_name='actor')
    tar = models.Relationship('Entity', rel_type=Outgoing.TARGET, related_single=True, related_name='target')
    content_type = models.Relationship('ContentType', rel_type=Outgoing.CONTENT_TYPE, related_single=True, related_name='type')
    content = models.StringProperty(max_length=255)
    date_time = models.DateTimeProperty()
    def __unicode__(self):
        return u"%s_%s" % (self.actor, self.tar)

class Group(Entity):
    admin = models.Relationship('Student', rel_type=Outgoing.ADMIN, related_single=True, related_name='admin')
    student = models.Relationship('Student', rel_type=Outgoing.MEMBER, related_single=False, related_name='members')
    group_type = models.Relationship('GroupType', rel_type=Outgoing.GROUP_TYPE, related_single=True, related_name='group_type')
    group_name = models.StringProperty(max_length=128, indexed=True)
    require_admin_validation = models.IntegerProperty()
    date_creation = models.DateProperty()

    @classmethod
    def create(cls, name, req_validation):
        node = cls(group_name=name, require_admin_validatio=req_validation, date_creation=datetime.date.today())
        node.save()
        return node

    def __unicode__(self):
        return self.group_name

#========================================
# Person Entity
#========================================

class Professor(Person):
    # rating properties, quotes.
    pass

class Student(Person):
    drive = models.Relationship('Drive', rel_type=Outgoing.STUDENT_DRIVE, related_single=True, related_name='drive')
    rank = models.Relationship('Rank', rel_type=Outgoing.STUDENT_RANK, related_single=True, related_name='rank')
    friends = models.Relationship('Student', rel_type=Outgoing.FRIEND, related_single=False, related_name='friends')
    concentration = models.Relationship('Concentration', rel_type=Outgoing.STUDENT_CONCENTRATION, related_single=False, related_name='concentration')
    messages = models.Relationship('Message', rel_type=Outgoing.CONTAIN, related_single=False, related_name='contains')
    groups = models.Relationship('Group', rel_type=Outgoing.STUDENT_GROUPS, related_single=False, related_name='groups')
    achievements = models.Relationship('Achievement', rel_type=Outgoing.ACHIEVEMENT, related_single=False, related_name='achievements')
    user_name = models.StringProperty(max_length=30, indexed=True)
    password = models.StringProperty(max_length=128)
    display_picture = models.StringProperty(max_length=255)
    phone = models.StringProperty(max_length=30)
    birthday = models.DateProperty()
    about = models.StringProperty(max_length=255)
    veracity = models.IntegerProperty()
    is_active = models.IntegerProperty()
    is_verified = models.IntegerProperty()
    date_joined = models.DateTimeProperty()
    last_login = models.DateTimeProperty()
    verification_key = models.StringProperty(max_length=30)

    def verified(self):
        return self.is_verified

    def get_verification_key(self):
        return self.verification_key

    def activate_student(self):
        self.is_verified = 1
        self.save()

    def login(self, pw):
        if check_password(pw, self.password):
            self.last_login = datetime.datetime.now()
            self.save()
            return True
        return False

    def get_current_courses(self, student_id, term_id):
        course = self.objects.select_related()
        return course

    @classmethod
    def create(cls, first_name, last_name, email, password):
        now = datetime.datetime.now()
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for n in range(20));
        student = cls(first_name=first_name, last_name=last_name,
            user_name=email[:email.index('@')], email=email,
            password=make_password(password), veracity=0, is_active=True, is_verified=False,
            last_login=now, date_joined=now, verification_key=key)
        student.save()
        return student

#========================================
# Content Entity
#========================================

class Post(Content):
    attach = models.Relationship('Content', rel_type=Outgoing.ATTACHMENT, related_single=False, related_name='attachment')
    com = models.Relationship('Content', rel_type=Outgoing.POST_COMMENTS, related_single=False, related_name='comments')

class Message(Content):
    is_read = models.IntegerProperty()
    is_archived = models.IntegerProperty()

#========================================
# Group Entity
#========================================

class Course(Group):
    school = models.Relationship('School', rel_type=Outgoing.COURSE_SCHOOL, related_single=True, related_name='school')
    offerings = models.Relationship('Offering', rel_type=Outgoing.COURSE_OFFERINGS, related_single=False, related_name='offerings')
    code = models.StringProperty(max_length=10, indexed=True)
    course_name = models.StringProperty(max_length=64)
    def __unicode__(self):
        return self.code

class Offering(Group):
    course = models.Relationship('Course', rel_type=Outgoing.OFFERING_COURSE, related_single=False, related_name='course')
    offering_term = models.Relationship('Term', rel_type=Outgoing.OFFERING_TERM, related_single=True, related_name='offering_term')
    professor = models.Relationship('Professor', rel_type=Outgoing.OFFERING_PROFESSOR, related_single=True, related_name='professor')

class School(Group):
    address = models.Relationship('Address', rel_type=Outgoing.SCHOOL_ADDRESS, related_single=True, related_name='address')
    school_type = models.Relationship('SchoolType', rel_type=Outgoing.SCHOOL_TYPE, related_single=True, related_name='school_type')
    concentrations = models.Relationship('Concentration', rel_type=Outgoing.SCHOOL_CONCENTRATIONS, related_single=False, related_name='concentrations')
    courses = models.Relationship('Course', rel_type=Outgoing.SCHOOL_COURSES, related_single=False, related_name='courses')
    school = models.StringProperty(max_length=60)
    def __unicode__(self):
        return self.school

class Concentration(Group):
    school = models.Relationship('School', rel_type=Outgoing.CONCENTRATION_SCHOOL, related_single=True, related_name='school')
    concentration = models.StringProperty(max_length=30)
    def __unicode__(self):
        return self.concentration
