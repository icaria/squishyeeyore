import datetime
import neo4django
from django.db import models
from neo4django import Outgoing
from neo4django.db import models as gmodels

# Create your models here.
# This is a mixed model of a RDMS (Relational Database) and GDMS (Graphic Database)
# Everything associated with one single entity is stored in a relational structure,
# everything associated with connections between two entity is stored in the graph.

now = datetime.date.today()
YEAR = range(now.year, now.year-100, -1)

#========================================
# Location
#========================================
class SchoolType(models.Model):
    type = models.CharField(max_length=60)
    class Meta:
        db_table = "SchoolType"

class School(models.Model):
    type = models.ForeignKey(SchoolType)
    school = models.CharField(max_length=60)
    class Meta:
        db_table = "School"
    
    def __unicode__(self):
        return self.school

class Concentration(models.Model):
    school = models.ForeignKey(School)
    concentration = models.CharField(max_length=30)
    class Meta:
        db_table = "Concentration"

class Faculty(models.Model):
    school = models.ForeignKey(School)
    faculty = models.CharField(max_length=30)
    class Meta:
        db_table = "Faculty"

class Course(models.Model):
    faculty = models.ForeignKey(Faculty)
    code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=64)
    class Meta:
        db_table = "Course"

class Country(models.Model):
    country = models.CharField(max_length=30)
    class Meta:
        db_table = "Country"
    
class ProvinceState(models.Model):
    country = models.ForeignKey(Country)
    province_state = models.CharField(max_length=30)
    class Meta:
        db_table = "ProvinceState"

class Address(models.Model):
    school = models.ForeignKey(School)
    country = models.ForeignKey(Country)
    province_state = models.ForeignKey(ProvinceState,null=True)
    street_address = models.CharField(max_length=60)
    city = models.CharField(max_length=30)
    class Meta:
        db_table = "Address"
        
#========================================
# File Sharing & Storage
#========================================

class Drive(models.Model):
    size = models.IntegerField(max_length=20)
    class Meta:
        db_table = "Drive"
        
#========================================
# Core
#========================================

class Rank(models.Model):
    number_stars = models.IntegerField()
    title = models.CharField(max_length=30)
    class Meta:
        db_table = "Rank"

class Term(models.Model):
    term_choices = (
        ('W', 'Winter'),
        ('S', 'Spring'),
        ('F', 'Fall'),
    )
    term = models.CharField(max_length=1)
    year = models.IntegerField()
    class Meta:
        db_table = "Term"

class Professor(models.Model):
    faculty = models.ForeignKey(Faculty)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    class Meta:
        db_table = "Professor"

class Offering(models.Model):
    course = models.ForeignKey(Course)
    term = models.ForeignKey(Term)
    professor = models.ForeignKey(Professor)
    class Meta:
        db_table = "Offering"

class Profile(models.Model):
    rank = models.ForeignKey(Rank)
    school = models.ForeignKey(School)
    drive = models.ForeignKey(Drive)
    concentration = models.ForeignKey(Concentration)
    average = models.DecimalField(max_digits=3, decimal_places=1)
    display_picture = models.CharField(max_length=255, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    birthday = models.DateField()
    about = models.CharField(max_length=255)
    class Meta:
        db_table = "Profile"

class Student(models.Model):
    profile = models.ForeignKey(Profile, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30, unique=True, null=True, blank=True)
    email = models.CharField(max_length=75,unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField()
    class Meta:
        db_table = "Student"

class Transcript(models.Model):
    student = models.ForeignKey(Student)
    offering = models.ForeignKey(Offering)
    grade = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1)
    weight = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2)
    hidden = models.BooleanField(default=False)
    class Meta:
        db_table = "Transcript"

class VerificationKey(models.Model):
    student = models.ForeignKey(Student)
    key = models.CharField(max_length=30)
    class Meta:
        db_table = "VerificationKey"

#========================================
# Groups and Pages
#========================================

class GroupType(models.Model):
    type = models.CharField(max_length=30)
    class Meta:
        db_table = "GroupType"

class Group(models.Model):
    type = models.ForeignKey(GroupType)
    admin = models.ForeignKey(Student, null=True, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True)
    school = models.ForeignKey(School, null=True, blank=True)
    name = models.CharField(max_length=128)
    require_admin_validation = models.BooleanField(default=False)
    date_creation = models.DateTimeField()
    class Meta:
        db_table = "Group"

class NewsFeed(models.Model):
    group = models.ForeignKey(Group)
    student = models.ForeignKey(Student)
    message = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = "NewsFeed"
        
class Inbox(models.Model):
    number_message = models.IntegerField(max_length=11)
    has_new = models.BooleanField(default=False)
    class Meta:
        db_table = "Inbox"

class Message(models.Model):
    inbox = models.ForeignKey(Inbox)
    sender = models.ForeignKey(Student, related_name='sender')
    receiver = models.ForeignKey(Student, related_name='receiver')
    message = models.CharField(max_length=255)
    send_date = models.DateTimeField()
    is_read = models.BooleanField(default=False)
    class Meta:
        db_table = "Message"
        
class Attachment(models.Model):
    newsfeed = models.ForeignKey(NewsFeed)
    filename = models.CharField(max_length=255)
    class Meta:
        db_table = "Attachment"

#========================================
# The Fun Stuff
#========================================

class Activity(models.Model):
    activity = models.CharField(max_length=64)
    class Meta:
        db_table = "Activity"

class ActivityCount(models.Model):
    student = models.ForeignKey(Student)
    activity = models.ForeignKey(Activity)
    count = models.IntegerField(max_length=11)
    class Meta:
        db_table = "ActivityCount"

class Notification(models.Model):
    student = models.ForeignKey(Student)
    notification = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    class Meta:
        db_table = "Notification"

class Achievement(models.Model):
    description = models.CharField(max_length=120)
    requirement = models.CharField(max_length=255)
    class Meta:
        db_table = "Achievement"

class TrophyCase(models.Model):
    student = models.ForeignKey(Student)
    achievement = models.ForeignKey(Achievement)
    class Meta:
        db_table = "TrophyCase"
             
#========================================
# People Graph
#========================================

class StudentNode(gmodels.NodeModel):
    friend = gmodels.Relationship('StudentNode', rel_type=Outgoing.FRIEND, single=False, related_name='friend')
    group = gmodels.Relationship('GroupNode', rel_tyle=Outgoing.MEMBER_OF, single=False, related_name='group')
    id = gmodels.IntegerProperty()

class GroupNode(gmodels.NodeModel):
    student = gmodels.Relationship('StudentNode', rel_type=Outgoing.MEMBER, single=False, related_name='member')
    id = gmodels.IntegerProperty()
