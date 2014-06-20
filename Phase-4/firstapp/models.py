from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Feedback_Questions(models.Model):
	ques = models.CharField(max_length=300)
	category = models.IntegerField()

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
    rating_sum = models.IntegerField()
    rated_concepts = models.IntegerField()
    def __unicode__(self):
	return self.name

class Feedback(models.Model):
	student = models.ForeignKey(Student)
	question = models.ForeignKey(Feedback_Questions)
	response = models.IntegerField()


def update_student_state(sender, instance, **kwargs):
    state_list = StudentState.objects.filter(course_id = instance.id)
    if not state_list:
	student_list = Student.objects.all()
	for student in student_list:
		student_state = StudentState(student_id= student.id,course_id = instance.id,KL=0.0,unknown=1.0,unsat_known=0.0,known=0.0,learned=0.0)
		student_state.save()
		student.rated_concepts += 1
		rr = Ratings(student = student, item = instance, rating = 0)
		rr.save()

	course_list = Course.objects.all()
    for course in course_list :
		if course != instance :
			cd = CourseDependency(course_source=course, course_target=instance, value=0, total_stu=0, average_change = 0, similarity = 0)
			cd.save()
			cd1 = CourseDependency(course_source=instance, course_target=course, value=0, total_stu=0, average_change = 0, similarity = 0)
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
    similarity = models.DecimalField(max_digits=10, decimal_places=5)
    
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

class Question_Concept(models.Model):
    question = models.ForeignKey(Question)
    concept = models.ForeignKey(Course)
    value = models.DecimalField(max_digits=3,decimal_places=2)

class Question_Concept_new(models.Model):
	question = models.ForeignKey(Question)
	concept = models.ForeignKey(Course)
	value = models.DecimalField(max_digits=3,decimal_places=2)

class Grade(models.Model):
        conceptID =  models.ForeignKey(Course)
	questionID = models.ForeignKey(Question)
	studentID = models.ForeignKey(Student)
	value = models.IntegerField()
	prev = models.IntegerField()
	attempted = models.IntegerField()

class ConfidenceRtoR(models.Model):
	questionSource = models.ForeignKey(Question, related_name="sourceR")
	questionTarget = models.ForeignKey(Question, related_name="targetR")
	confidenceValue = models.DecimalField(max_digits=3,decimal_places=2)

class ConfidenceWtoW(models.Model):
	questionSource = models.ForeignKey(Question, related_name="sourceW")
	questionTarget = models.ForeignKey(Question, related_name="targetW")
	confidenceValue = models.DecimalField(max_digits=3,decimal_places=2)

class Q1Q2RightWrong(models.Model):
	question_x = models.ForeignKey(Question, related_name="id1")
	question_y = models.ForeignKey(Question, related_name="id2")
	right = models.IntegerField()
	wrong = models.IntegerField()

class Ratings(models.Model):
	student = models.ForeignKey(Student)
	item = models.ForeignKey(Course)
	rating = models.IntegerField()

class Student_History(models.Model):
	student = models.ForeignKey(Student)
	concept = models.ForeignKey(Course)
	score = models.DecimalField(max_digits=3,decimal_places=2)
	last_update = models.DateTimeField(auto_now=True)

class Student_Similarity(models.Model):
	student1 = models.ForeignKey(Student, related_name="student1")
	student2 = models.ForeignKey(Student, related_name="student2")
	similarity = models.DecimalField(max_digits=3,decimal_places=2)
