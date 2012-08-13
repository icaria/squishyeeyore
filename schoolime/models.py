from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=60)
    class Meta:
        db_table = "School"

class Country(models.Model):
    country = models.CharField(max_length=60)
    class Meta:
        db_table = "Country"
    
class ProvinceState(models.Model):
    country = models.ForeignKey(Country)
    province_state = models.CharField(max_length=60)
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

class Student(models.Model):
    school = models.ForeignKey(School)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75,unique=True)
    phone = models.IntegerField(unique=True, blank=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = "Student"

class Term(models.Model):
    term = (
        ('W', 'Winter'),
        ('S', 'Spring'),
        ('F', 'Fall'),
    )
    term = models.CharField(max_length=1)
    year = models.IntegerField()
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
    
class Offering(models.Model):
    course = models.ForeignKey(Course)
    term = models.ForeignKey(Term)
    class Meta:
        db_table = "Offering"

class Transcript(models.Model):
    student = models.ForeignKey(Student)
    offering = models.ForeignKey(Offering)
    grade = models.IntegerField(blank=True)
    class Meta:
        db_table = "Transcript"
    
