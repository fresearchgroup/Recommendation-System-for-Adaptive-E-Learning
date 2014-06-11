import time

from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from firstapp.models import *
import datetime
from django.shortcuts import render, render_to_response
from firstapp.forms import CourseAddForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Min, Q
from firstapp.tasks import concept_map

def login_form(request):
	return render(request, 'login.html')

def login_handler(request):
	if 'username' in request.GET and request.GET['username']:
		username = request.GET['username']
	else:
		return render(request, 'login.html', {'error':True})
	
	if 'password1' in request.GET and request.GET['password1']:
		password = request.GET['password1']
	else:
		return render(request, 'login.html', {'error':True})

	user = authenticate(username = username, password = password)
	
	if user is not None:
		if user.is_active:
			message = "You provided a correct username and password!"
			request.session['logged_in'] = 1
			request.session['login_id'] = user.id
			print user.is_staff
			request.session['staff_mode'] = user.is_staff
			if user.is_staff==0: 
				return HttpResponseRedirect("/concept_menu/")
			else:
				return HttpResponseRedirect("/staff_menu/")
		else:
			message = "Your account has been dsabled!"
	else:
		return render(request, 'login.html', {'error':True})

	return HttpResponse(message)
		

def registeration_form(request):
	return render(request, 'registeration.html')

def logout_handler(request):
	if 'logged_in' in request.session : 	
		del request.session['logged_in']
	if 'login_id' in request.session : 
		del request.session['login_id']
	if 'course_id' in request.session : 	
		del request.session['course_id']
	if 'staff_mode' in request.session : 	
		del request.session['staff_mode']
	
	return HttpResponseRedirect("/login-form") 

def signup_handler(request):
	if 'username' in request.GET and request.GET['username']:
		username = request.GET['username']

	else:
		return render(request, 'registeration.html', {'error1':True})
	
	if 'email' in request.GET and request.GET['email']:
		email = request.GET['email']

	else:
		return render(request, 'registeration.html', {'error1':True})

	if 'password1' in request.GET and request.GET['password1']:
		password = request.GET['password1']

	else:
		return render(request, 'registeration.html', {'error1':True})
	
	if 'password2' in request.GET and request.GET['password2']:
		confirm_password = request.GET['password2']

	else:
		return render(request, 'registeration.html', {'error1':True})

	if password == confirm_password	:

		user = User.objects.create_user(username, email, password)
		user.save()
		student = Student(user_id=user.id,name=user.username,content_preference='pdf', prev_course=Course.objects.get(name='foundation'), rating_sum = 0, rated_concepts = Course.objects.all().count())
		student.save()
		message = "You have been saved.."
		course_list = Course.objects.all();
		for course in course_list:
			if course.name == 'foundation' :
				state = StudentState(student_id=student.id, course_id=course.id, KL=1.0, unknown=0.0, unsat_known=0.0, known=0.0, learned=1.0)
			else :
				state = StudentState(student_id=student.id, course_id=course.id, KL=0.0, unknown=1.0, unsat_known=0.0, known=0.0, learned=0.0)
			state.save()
			rr = Ratings(student = student, item = course, rating = 0)
			rr.save()
		questionList = Question.objects.all()
		for question in questionList:
			grade = Grade(studentID=student,questionID=question,value=0,prev=0)
			grade.save()
		
		questionList = Question.objects.all()		
		length = len(questionList)
		i = 0
		while i < length:
			j = i + 1
			question1 = questionList[i]
			while j < length:
				question2 = questionList[j]
				if question2.id == question1.id:
					continue
				object3 = Q1Q2RightWrong.objects.get(question_x=question1, question_y=question2)
				object3.wrong = object3.wrong + 1
				object3.save()
				j = j + 1
			i = i + 1

		for question in questionList:
			object3 = Q1Q2RightWrong.objects.get(question_x=question, question_y=question)
			object3.wrong = object3.wrong + 1
			object3.save()
		
		request.session['login_id'] = user.id
		request.session['logged_in'] = 1
		request.session['staff_mode'] = 0

		return HttpResponseRedirect('/concept_menu')

	else:
		return render(request, 'registeration.html', {'error1':True})	

def concept_menu_view(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form/")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")
	student  = Student.objects.get(user_id=request.session['login_id'])
	passed_c = StudentState.objects.filter(student_id = student.id, KL__gt=0.5)
	plist = []

	for element in passed_c :
		if element.course.name != 'foundation' :
			plist.append(element.course);
	concept_list = CourseDependency.objects.filter(course_source = student.prev_course).order_by('-average_change')

	clist = []
	for element in concept_list :
		if element.course_target.name != 'foundation' :
			clist.append(element.course_target)

	if student.prev_course not in plist :
		if student.prev_course.name != 'foundation' :
			clist.append(student.prev_course)

	#courses_rated = Ratings.objects.filter(student = student, item != student.prev_course)
	

	all_courses = Course.objects.all()


	class prediction:
		prediction_value = 0
		concept = 0

	predict_course_list = []

	for course_i  in all_courses :
		similar_list = CourseDependency.objects.filter(course_source = course_i).order_by('-similarity')
		#Choosing K
		k = 3

		numerator = 0
		denominator = 1
		count = 0
		for concept in similar_list :
			if count < k :
				numerator += concept.similarity * Ratings.objects.get(student = student, item = concept.course_target).rating
			count = count + 1
			denominator += float(concept.similarity) ** 2

		denominator = float(denominator) ** 0.5
	
		temp = prediction()
		temp.prediction_value = float(numerator)/float(denominator);
		temp.concept = course_i
		predict_course_list.append(temp)

	predict_course_list.sort(key=lambda x: x.prediction_value, reverse = True)

	#print ("plist")
	#print (plist)

	#print("clist")
	#print(clist)
	print "predict_course_list"
	for ii in predict_course_list :
		print str(ii.concept) + str(" ") + str(ii.prediction_value)
	print predict_course_list
	return render(request, 'concept_menu.html',{'concept_list':clist, 'passed_list':plist, 'student_name' : student.name, 'cf_predict_list' : predict_course_list})
def concept_submenu_view(request, course_id):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")
	
	try:
		course_id = int(course_id)
	except:
		raise Http404()
	request.session['course_id'] = course_id
	student_name = Student.objects.get(user_id=request.session['login_id']).name
	return render(request,'concept_submenu.html',{'student_name' : student_name})

def pdf_view(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")
	if 'course_id' not in request.session:
		return HttpResponseRedirect("/concept_menu") 
	
	filename = str(Course.objects.get(id=request.session['course_id']).content)
	with open('/home/devanshu/summer_django_iitb/mysite/media/'+filename,'r') as pdf:
		response = HttpResponse(pdf.read(),mimetype='application/pdf')
		response['Content-Disposition'] = 'inline;filename=some_file.pdf'
		return response
	pdf.closed		

def performance_view(request) :
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")
		
	studentid = Student.objects.get(user_id=request.session['login_id'])
	state_list = StudentState.objects.filter(student_id=studentid)
	course_list = Course.objects.all()
	student_name = Student.objects.get(user_id=request.session['login_id']).name
	return render(request, 'performance.html', {'course_list':course_list,'state_list':state_list, 'student_name':student_name})

def quiz_view(request):
		
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")
	if 'course_id' not in request.session:
		return HttpResponseRedirect("/concept_menu")
	questionlist = Question.objects.filter(course_id = request.session['course_id'])
	coursename = Course.objects.get(id = request.session['course_id']).name
	student_name = Student.objects.get(user_id=request.session['login_id']).name
	return render(request,'quiz.html',{'coursename':coursename,'question_list':questionlist,'student_name':student_name, 'range_rate': range(1, 11)})

def evaluate_quiz_view(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")
	if 'course_id' not in request.session:
		return HttpResponseRedirect("/concept_menu")
	questionlist = Question.objects.filter(course_id = request.session['course_id'])

	student = Student.objects.get(user_id=request.session['login_id'])
	studentid = student.id
	studentstate_list = StudentState.objects.filter(student_id=studentid)

	score = 0
	num_of_questions = 0
	for question in questionlist:
		num_of_questions=num_of_questions+1
		chosen = request.GET.get(str(question.id))	

		if not chosen:
			messages.error(request, 'Please attempt all questions before submitting.')
			return HttpResponseRedirect('/quiz/')
		chosen = int(chosen)

		try:
			gradeObject = Grade.objects.get(questionID = question.id, studentID = studentid)
		except Grade.DoesNotExist:
			gradeObject = Grade(questionID=question, studentID=student, value=0)

		if chosen == question.answer:
			score=score+1
			gradeObject.prev = gradeObject.value
			gradeObject.value=1
		else:
			gradeObject.prev = gradeObject.value
			gradeObject.value=0
		gradeObject.save()

	print 'score = ' + str(score)

	course_id = int(request.session['course_id'])
	#print "course_id = " + str(course_id)



	concept_map.delay(course_id, student)

	knowledge = float(score)/num_of_questions
	knowledge = int(knowledge * 100)
	knowledge = float(knowledge)/100

	sumKL = -1
	for studentstate in studentstate_list :
		sumKL = sumKL + float(studentstate.KL)
		#print(studentstate.course.name)
		#print(sumKL)

	#print("SumKl Before")
	#print(sumKL)
	
	studentstate_this_course = StudentState.objects.get(student_id = studentid,course_id=request.session['course_id'])
	
	oldKL = float(studentstate_this_course.KL)
	studentstate_this_course.KL = knowledge
	studentstate_this_course.save()
	update_student_state(studentstate_this_course)

	message = "new"
	noOfCourse = 0
	for studentstate in studentstate_list:
		noOfCourse = noOfCourse + 1
		if (studentstate.course_id is not request.session['course_id']) and (studentstate.course.name != 'foundation'):
			dependency = CourseDependency.objects.filter(course_source_id=request.session['course_id'],course_target_id=studentstate.course_id)
			if dependency:
					if oldKL==0:
						change = knowledge*float(dependency[0].value)
						studentstate.KL = change
						if studentstate.KL>1:
							studentstate.KL = 1
						if studentstate.KL<0:
							studentstate.KL = 0
						studentstate.save()
						update_student_state(studentstate)
					else:
						change = (knowledge-oldKL)*(float(dependency[0].value))/oldKL
						studentstate.KL = float(studentstate.KL)
						studentstate.KL = (studentstate.KL) + (studentstate.KL)*change
						if studentstate.KL>1:
							studentstate.KL = 1
						if studentstate.KL<0:
							studentstate.KL = 0						
						studentstate.save()
						update_student_state(studentstate)

	sumFL = 0
	for studentstate in StudentState.objects.filter(student_id=studentid) :
		if studentstate.course.name != 'foundation' :
			sumFL = sumFL + float(studentstate.KL)
		#print(studentstate.course.name)
		#print(sumFL)

	#print("Final Sum")
	#print(sumFL)

	diff = float(sumFL) - float(sumKL)
	diff = diff / (noOfCourse - 1)
	curr_stu = Student.objects.get(user_id=request.session['login_id'])

	print "prev_id" + str(curr_stu.prev_course.id)
	print "course_id" + str(request.session['course_id'])	

	if (curr_stu.prev_course.id != request.session['course_id']) :
		dep = CourseDependency.objects.get(course_source_id = curr_stu.prev_course.id, course_target_id = request.session['course_id'])
		dep.average_change = ((float(dep.average_change)*float(dep.total_stu)) + diff)/ (float(dep.total_stu) + 1) 
		dep.total_stu = dep.total_stu + 1;
		dep.save()

	if knowledge >= 0.5 : 
		curr_stu.prev_course = Course.objects.get(id = request.session['course_id'])
		curr_stu.save()


	curr_item = Course.objects.get(id = request.session['course_id'])
	rate = request.GET["rate"]
	rr = Ratings.objects.get(student=curr_stu, item =curr_item)
	curr_stu.rating_sum -= rr.rating
	curr_stu.rating_sum += int(rate)
	curr_stu.save()
	rr.rating = int(rate)
	rr.save()

	dest_list = CourseDependency.objects.filter(course_source = curr_item)
	list_i = Ratings.objects.filter(item = curr_item)

	for sim in dest_list :
		numerator = 0
		denominator1 = 0
		denominator2 = 0		
		for rater in list_i :
			print "rater.student.rated_concepts : " + str(rater.student.rated_concepts)
			rater_u_avg = float(rater.student.rating_sum)/float(rater.student.rated_concepts)
			rater_u_i = rater.rating
			print "sim = "
			rater_u_j = Ratings.objects.get(item = sim.course_target, student = rater.student).rating
			
			numerator += (rater_u_i - rater_u_avg)*(rater_u_j - rater_u_avg)
			denominator1 += (rater_u_i - rater_u_avg)**2
			denominator2 += (rater_u_j - rater_u_avg)**2

		try:
			similarity = float(numerator) / ((float(denominator1)**0.5)*(float(denominator2)**0.5))
		except ZeroDivisionError:
			similarity = 0

		dep1 = CourseDependency.objects.get(course_source = curr_item, course_target = sim.course_target)
		dep2 = CourseDependency.objects.get(course_source = sim.course_target, course_target = curr_item)

		dep1.similarity = similarity
		dep2.similarity = similarity

		dep1.save()
		dep2.save()

	score = knowledge * 100

	if course_id == 12:
		return render(request, 'quiz_result1.html', {'score':score})
	if course_id == 13:
		return render(request, 'quiz_result2.html', {'score':score})
	if course_id == 14:
		return render(request, 'quiz_result3.html', {'score':score})
	if course_id == 15:
		return render(request, 'quiz_result4.html', {'score':score})


def staff_menu_view(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 0:
		return HttpResponseRedirect("/concept_menu/")
	staff_name = User.objects.get(id=request.session['login_id']).username
	return render(request, 'staff_menu.html',{'staff_name':staff_name})


def add_concept_view(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 0:
		return HttpResponseRedirect("/concept_menu/")
	if request.method == 'POST':
		print("hello")		
		form = CourseAddForm(request.POST, request.FILES)
		if request.FILES:		
			print("hello2")			
			instance = Course(name=request.POST.get('filename'), content=request.FILES['myfile'])		
			instance.save()
			return HttpResponse('Your file has been saved.Please <a href="/staff_menu/">click</a> to continue...')
		else:
			form = CourseAddForm()	
			messages.error(request, "You haven't selected anything..")		
	else:
		form = CourseAddForm()
	staff_name = User.objects.get(id=request.session['login_id']).username
	return render(request, 'add_course.html', {'form':form,'staff_name':staff_name})

def concept_upload_handler(request):  
	return HttpResponse("under construction")

def delete_concept_view(request):
    return HttpResponse("Under Construction")

def concept_deletion_handler(request):
	return HttpResponse("Under Construction")

def add_question_view(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 0:
		return HttpResponseRedirect("/concept_menu/")
	
	course_list = Course.objects.all()
	staff_name = User.objects.get(id=request.session['login_id']).username
	return render(request, 'add_question.html',{'course_list':course_list, 'staff_name':staff_name})

def question_upload_handler(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 0:
		return HttpResponseRedirect("/concept_menu/")
	course = Course.objects.get(id=int(request.GET.get('course')))
	question = request.GET.get('question')
	option1 = request.GET.get('option1')
	option2 = request.GET.get('option2')
	option3 = request.GET.get('option3')
	option4 = request.GET.get('option4')
	answer = request.GET.get('answer')
	if not course or not question or not option1 or not option2 or not option3 or not option4 or not answer :
		messages.error(request, "You can't leave anything blank.")
		return HttpResponseRedirect('/add_question/')
		
	q = Question(course=course, question=question, option1=option1, option2=option2, option3=option3, option4=option4, answer=answer)
	q.save()
	return HttpResponse('Your question has been saved.Please <a href="/staff_menu/">click</a> to continue...')

def edit_question_view(request):
	return HttpResponse("Site Under Construction")

def delete_question_view(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 0:
		return HttpResponseRedirect("/concept_menu/")	
	question_list = Question.objects.all()
	staff_name = User.objects.get(id=request.session['login_id']).username
	return render(request,'delete_question.html',{'question_list':question_list, 'staff_name':staff_name})

def question_deletion_handler(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 0:
		return HttpResponseRedirect("/concept_menu/")	
	for question in Question.objects.all():
		if request.GET.get(str(question.id)):
			question.delete()
	return HttpResponse('Your request has been processed.Please <a href="/staff_menu/">click</a> to continue...') 

def feedback_view(request):
	student_name = Student.objects.get(user_id=request.session['login_id']).name
	return render(request, 'feedback.html',{'student_name':student_name})

def feedback_handler(request) :
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")

	feedback = Feedback()	

	course_id = request.session['course_id']

	if course_id == 12:
		feedback1(request)
	if course_id == 13:
		feedback2(request)
	if course_id == 14:
		feedback3(request)
	if course_id == 15:
		feedback4(request)
	return(HttpResponse('Thank you for your feedback. Click <a href = "/concept_menu">here</a> to continue'))

def feedback1(request):		
	feedback = Feedback(q1=request.GET.get('1'), q2=request.GET.get('2'), q3=request.GET.get('3'), q4=request.GET.get('4'))
	feedback.save()
	
def feedback2(request):
	feedback = Feedback(q5=request.GET.get('5'), q6=request.GET.get('6'), q7=request.GET.get('7'), q8=request.GET.get('8'))
	feedback.save()

def feedback3(request):
	feedback = Feedback(q5=request.GET.get('9'), q6=request.GET.get('10'), q7=request.GET.get('11'), q8=request.GET.get('12'))
	feedback.save()

def feedback4(request):
	feedback = Feedback(q5=request.GET.get('13'), q6=request.GET.get('14'), q7=request.GET.get('15'))
	feedback.save()
		
def add_stuff(request):
	
	List = Question.objects.all()

	print len(List)
		
	List2 = Course.objects.all()	

	print len(List2)

	List3 = Question_Concept.objects.all()
	for item in List3:
		item.delete()

	List3 = Question_Concept_new.objects.all()
	for item in List3:
		item.delete()

	counter = 0

	for question in List:
		counter = counter + 1
		counter2 = 0
		for concept in List2:
			
			if counter%2 == 0:
				if counter2%2 == 0:
					object1 = Question_Concept(question=question,concept=concept,value=0.5)
				else:
					object1 = Question_Concept(question=question,concept=concept,value=0)
			else:
				if counter2%2 == 0:
					object1 = Question_Concept(question=question,concept=concept,value=0)
				else:
					object1 = Question_Concept(question=question,concept=concept,value=0.5)									
			counter2 = counter2 + 1
			object1.save()

	counter = 0

	question_concept_list = Question_Concept.objects.all()
	for item in question_concept_list:
		question = item.question
		concept = item.concept
		value = item.value
		vertical_column = Question_Concept.objects.filter(concept=concept)
		sum1 = 0
		for item2 in vertical_column:
			sum1 += item2.value
		if sum1 > value:
			value = value / sum1
		object1 = Question_Concept_new(question=question,concept=concept,value=value)
		object1.save()

#	for question in List:
#		counter = counter + 1
#		counter2 = 0
#		for concept in List2:
#			
#			if counter%2 == 0:
#				if counter2%2 == 0:
#					object1 = Question_Concept_new(question=question,concept=concept,value=0.5)
#				else:
#					object1 = Question_Concept_new(question=question,concept=concept,value=0)
#			else:
#				if counter2%2 == 0:
#					object1 = Question_Concept_new(question=question,concept=concept,value=0)
#				else:
#					object1 = Question_Concept_new(question=question,concept=concept,value=0.5)									
#			counter2 = counter2 + 1
#			object1.save()

	

	return HttpResponse('Your Stuff has been added') 


def update_student_state(studentstate):
	u_un = studentstate.unknown
	u_uk = studentstate.unsat_known
	u_k = studentstate.known
	u_l = studentstate.learned
	kl = float(studentstate.KL) * 100
	
# for unknown

	if kl <= 55 :
		u_un = 1
	elif kl > 55 and kl < 60 :
		u_un = (1 - (kl - 55)/5)
	elif kl >= 60 :
		u_un = 0

# for unsatisfactorily known

	if kl <= 55 or kl >= 75 :
		u_uk = 0
	elif kl > 55 and kl < 60 : 
		u_uk = (kl - 55)/5
	elif kl >= 60 and kl <= 70 :
		u_uk = 1
	elif kl > 70 and kl < 75 :
		u_uk = (1 - (kl - 70)/5)

# for known

	if kl <= 70 or kl >= 90 :
		u_k = 0
	elif kl > 70 and kl < 75 : 
		u_k = (kl - 70)/5
	elif kl >= 75 and kl <= 85 : 
		u_k = 1
	elif kl > 85 and kl < 90 :
		u_k = (1 - (kl - 85)/5)
# for learned

	if kl <= 85 :
		u_l = 0
	elif kl > 85 and kl < 90 :
		u_l = (kl - 85)/5
	elif kl >= 90 or kl <= 100 :
		u_l = 1

	studentstate.unknown = u_un
	studentstate.unsat_known = u_uk
	studentstate.known = u_k
	studentstate.learned = u_l
	studentstate.save()


