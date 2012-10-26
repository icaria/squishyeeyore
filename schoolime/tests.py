"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
from schoolime.models import Student
from schoolime.models import Course
from schoolime.models import Offering
from neo4django import testutils

class StudentTest(testutils.NodeModelTestCase):
    def setUp(self):
        self.student_node = Student.objects.create(first_name='Stephen', last_name='Chen', email='efrt')
        self.course_node = Course.objects.create(code='CS133', course_name="Test Course")
        self.offering_node = Offering.objects.create(name='ABCD')

    def tearDown(self):
        pass

    def test_student_can_add_course_offering_as_groups(self):
        self.student_node.groups.add(self.course_node)
        self.student_node.groups.add(self.offering_node)
        self.student_node.save()

        groupList = list(self.student_node.groups.all())

        self.assertEqual(len(groupList), 2)
        self.assertTrue(self.course_node in groupList)
        self.assertTrue(self.offering_node in groupList)

class SimpleTest(unittest.TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
