from django.db import models

# Create your models here.

#========================================
# Location
#========================================
class School(models.Model):
    name = models.CharField(max_length=60)
    class Meta:
        db_table = "School"

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

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75,unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField()
    class Meta:
        db_table = "Student"

class Profile(models.Model):
    student = models.ForeignKey(Student)
    rank = models.ForeignKey(Rank)
    school = models.ForeignKey(School)
    phone = models.IntegerField(unique=True, blank=True)
    birthday = models.DateField()
    about = models.CharField(max_length=256)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = "Profile"

class Term(models.Model):
    term = (
        ('W', 'Winter'),
        ('S', 'Spring'),
        ('F', 'Fall'),
    )
    term = models.CharField(max_length=1)
    year = models.IntegerField()
    is_current = models.BooleanField()
    class Meta:
        db_table = "Term"

class Faculty(models.Model):
    school = models.ForeignKey(School)
    name = models.CharField(max_length=30)
    class Meta:
        db_table = "Faculty"

class Course(models.Model):
    faculty = models.ForeignKey(Faculty)
    code = models.IntegerField()
    name = models.CharField(max_length=30)
    class Meta:
        db_table = "Course"

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

