"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from schoolime.models import Student
from schoolime.models import Course
from schoolime.models import Offering
from schoolime.models import Term
from neo4django import testutils

class StudentTest(testutils.NodeModelTestCase):
    def setUp(self):
        self.student_node = Student.objects.create(first_name='Stephen', last_name='Chen', email='stephenchen0@gmail.com')
        self.course_node = Course.objects.create(group_name='CS133', code='CS133', course_name="Test Course")
        self.offering_node = Offering.objects.create(group_name='CS133')
        self.term_node = Term.objects.create(year=2013, term_letter='F')
        self.offering_node.offering_term.add(self.term_node)
        self.offering_node.save()

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

    def test_can_query_student_by_email(self):
        student = Student.objects.get(email='stephenchen0@gmail.com')
        self.assertIsNotNone(student)

    def test_can_query_student_group_by_id(self):
        self.student_node.groups.add(self.course_node)
        self.student_node.groups.add(self.offering_node)
        self.student_node.save()

        c = self.student_node.groups.filter(id=self.course_node.id)[0]
        self.assertIsNotNone(c)
        self.assertEqual(c.group_name, 'CS133')

    def test_can_remove_existing_relationship(self):
        self.student_node.groups.add(self.course_node)
        self.student_node.groups.add(self.offering_node)
        self.student_node.save()

        course = Course.objects.get(id=self.course_node.id)

        self.student_node.groups.remove(course)
        groupList = list(self.student_node.groups.all())

        self.assertEqual(len(groupList), 1)
        self.assertFalse(self.course_node in groupList)
        self.assertTrue(self.offering_node in groupList)

    def test_student_offering_can_be_queried_by_domain(self):
        self.student_node.groups.add(self.course_node)
        self.student_node.groups.add(self.offering_node)
        self.student_node.save()


        list = list().get(offering_term__contains=self.term_node)#objects.filter(offering_term__contains=self.term_node)
        print self.term_node

        #list = Offering.objects.select_related(term=)
        #assert len(list) != 0

#        node = Student.objects.get(id=self.student_node.id).()

#        assert len(node) != 0

class TermTest(testutils.NodeModelTestCase):

    def test_can_create_node_with_get_or_create(self):
        (node, isCreated) = Term.objects.get_or_create(year=2013, term_letter="W")

        assert(isCreated is True)

        assert node.term_letter == "W"
        assert node.year == 2013

