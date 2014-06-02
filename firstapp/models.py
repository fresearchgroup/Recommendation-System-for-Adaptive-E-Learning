from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Feedback(models.Model):
    q1 = models.CharField(max_length=1)
    q2 = models.CharField(max_length=1)
    q3 = models.CharField(max_length=1)
    q4 = models.CharField(max_length=1)
    q5 = models.CharField(max_length=1)
    q6 = models.CharField(max_length=1)
    q7 = models.CharField(max_length=1)
    q8 = models.CharField(max_length=1)
    q9 = models.CharField(max_length=1)
    q10 = models.CharField(max_length=1)
    q11 = models.CharField(max_length=1)
    q12 = models.CharField(max_length=1)
    q13 = models.CharField(max_length=1)
    q14 = models.CharField(max_length=1)
    q15 = models.CharField(max_length=1)

class Course(models.Model):
    name = models.CharField(max_length=30)
    content = models.FileField(upload_to='documents/')
    def __unicode__(self):
	return self.name


class Student(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    content_preference = models.CharField(max_length=30)
    prev_course = models.ForeignKey(Course)
    def __unicode__(self):
	return self.name

def update_student_state(sender, instance, **kwargs):
    state_list = StudentState.objects.filter(course_id = instance.id)
    if not state_list:
	student_list = Student.objects.all()
	for student in student_list:
		student_state = StudentState(student_id= student.id,course_id = instance.id,KL=0.0,unknown=1.0,unsat_known=0.0,known=0.0,learned=0.0)
		student_state.save()
	

	course_list = Course.objects.all()
    for course in course_list :
		if course != instance :
			cd = CourseDependency(course_source=course, course_target=instance, value=0, total_stu=0, average_change=0)
			cd.save()
			cd1 = CourseDependency(course_source=instance, course_target=course, value=0, total_stu=0, average_change=0)
			cd1.save()
	
# register the signal
post_save.connect(update_student_state, sender=Course, dispatch_uid="new_course_added")

class StudentState(models.Model):
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    KL = models.DecimalField(max_digits=3,decimal_places=2)
    unknown = models.DecimalField(max_digits=3,decimal_places=2)
    unsat_known = models.DecimalField(max_digits=3,decimal_places=2)
    known = models.DecimalField(max_digits=3,decimal_places=2)
    learned = models.DecimalField(max_digits=3,decimal_places=2)

class CourseDependency(models.Model):
    course_source = models.ForeignKey(Course, related_name="source")
    course_target = models.ForeignKey(Course, related_name="target")
    value = models.DecimalField(max_digits=3,decimal_places=2)
    total_stu = models.IntegerField()
    average_change = models.DecimalField(max_digits=3,decimal_places=2)

class Question(models.Model):
    course = models.ForeignKey(Course)
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=40)
    option2 = models.CharField(max_length=40)
    option3 = models.CharField(max_length=40)
    option4 = models.CharField(max_length=40)
    answer = models.IntegerField()
    def __unicode__(self):
	return self.question

class Grade(models.Model):
	questionID = models.ForeignKey(Question)
	studentID = models.ForeignKey(Student)
	value = models.IntegerField()
	rating = models.IntegerField()
