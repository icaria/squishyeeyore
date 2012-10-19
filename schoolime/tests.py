"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
from schoolime.models import Student
from neo4django import testutils

class StudentTest(testutils.NodeModelTestCase):
    def setUp(self):
        self.user = Student.create("Stephen", "Chen", "stephenchen0@gmail.com", "57425962")

    def tearDown(self):
        pass

    def test_student_is_created(self):
        self.assertIsNotNone(self.user.pk)

class SimpleTest(unittest.TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
