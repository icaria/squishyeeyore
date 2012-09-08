import datetime
from django.db import models

# Create your models here.
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
    course_name = models.CharField(max_length=30)
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
# Coursewire
#========================================


class Rank(models.Model):
    number_stars = models.IntegerField()
    title = models.CharField(max_length=30)
    class Meta:
        db_table = "Rank"

class Profile(models.Model):
    rank = models.ForeignKey(Rank)
    school = models.ForeignKey(School)
    concentration = models.ForeignKey(Concentration)
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
    is_active = models.BooleanField()
    is_verified = models.BooleanField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = "Student"

class VerificationKey(models.Model):
    student = models.ForeignKey(Student)
    key = models.CharField(max_length=30)
    class Meta:
        db_table = "VerificationKey"

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
    
class Transcript(models.Model):
    student = models.ForeignKey(Student)
    offering = models.ForeignKey(Offering)
    grade = models.IntegerField(blank=True)
    class Meta:
        db_table = "Transcript"

#========================================
# Groups and Pages
#========================================

class GroupType(models.Model):
    type = models.CharField(max_length=30)
    class Meta:
        db_table = "GroupType"

class Group(models.Model):
    type = models.ForeignKey(GroupType)
    admin = models.ForeignKey(Profile, null=True, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True)
    school = models.ForeignKey(School, null=True, blank=True)
    name = models.CharField(max_length=128)
    require_admin_validation = models.BooleanField()
    date_creation = models.DateTimeField()
    class Meta:
        db_table = "Group"

class GroupMembership(models.Model):
    student = models.ForeignKey(Student)
    group = models.ForeignKey(Group)
    pending = models.BooleanField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = "GroupMembership"

#========================================
# File Sharing & Storage
#========================================

class Drive(models.Model):
    student = models.ForeignKey(Student)
    size = models.IntegerField(max_length=20)
    class Meta:
        db_table = "Drive"


#========================================
# The Fun Stuff
#========================================
    
class Activity(models.Model):
    student = models.ForeignKey(Student)
    class Meta:
        db_table = "Activity"

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

