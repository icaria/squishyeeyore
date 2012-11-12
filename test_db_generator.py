from schoolime.models import *

student_node = Student.create("Stephen", "Chen", "stephenchen0@gmail.com", "57425962")
student_node.activate_student()

curr_term = Term.get_current_term()

group_type = GroupType.objects.create(type="Offering")

course_node = Course.objects.create(name='CS246', description='Concurrent Programming')

offering_node = Offering.objects.create(name='CS246', description='Concurrent Programming')
offering_node.course = course_node
offering_node.offering_term = curr_term
offering_node.type = group_type
offering_node.save()

course_node.offerings.add(offering_node)
course_node.save()

student_node.groups.add(offering_node)
student_node.save()