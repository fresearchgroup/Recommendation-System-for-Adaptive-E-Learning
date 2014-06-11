from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from firstapp.models import Student, Course, StudentState, CourseDependency, Question, Feedback
import datetime
from django.shortcuts import render, render_to_response
from firstapp.forms import CourseAddForm
from django.contrib import messages
from django.core.urlresolvers import reverse

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
		student = Student(user_id=user.id,name=user.username,content_preference='pdf', prev_course=Course.objects.get(name='foundation'))
		student.save()
		message = "You have been saved.."
		course_list = Course.objects.all();
		for course in course_list:
			if course.name == 'foundation' :
				state = StudentState(student_id=student.id, course_id=course.id, KL=1.0, unknown=0.0, unsat_known=0.0, known=0.0, learned=1.0)
			else :
				state = StudentState(student_id=student.id, course_id=course.id, KL=0.0, unknown=1.0, unsat_known=0.0, known=0.0, learned=0.0)
			state.save()
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
		clist.append(student.prev_course)

	print ("plist")
	print (plist)

	print("clist")
	print(clist)

	return render(request, 'concept_menu.html',{'concept_list':clist, 'passed_list':plist, 'student_name' : student.name})

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
	return render(request,'quiz.html',{'coursename':coursename,'question_list':questionlist,'student_name':student_name})

def evaluate_quiz_view(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")
	if 'course_id' not in request.session:
		return HttpResponseRedirect("/concept_menu") 
	questionlist = Question.objects.filter(course_id = request.session['course_id'])
	score = 0
	num_of_questions = 0	
	for question in questionlist:
		num_of_questions=num_of_questions+1
		chosen = request.GET.get(str(question.id))	
		if not chosen:
			messages.error(request, 'Please attempt all questions before submitting.')
			return HttpResponseRedirect('/quiz/')
		chosen = int(chosen)
		if chosen == question.answer:
			score=score+1
	
	knowledge = float(score)/num_of_questions
	knowledge = int(knowledge * 100)
	knowledge = float(knowledge)/100

	studentid = Student.objects.get(user_id=request.session['login_id']).id
	studentstate_list = StudentState.objects.filter(student_id=studentid)

	print(studentstate_list)
	
	sumKL = -1
	for studentstate in studentstate_list :
		sumKL = sumKL + float(studentstate.KL)
		print(studentstate.course.name)
		print(sumKL)

	print("SumKl Before")
	print(sumKL)
	
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
		print(studentstate.course.name)
		print(sumFL)

	print("Final Sum")
	print(sumFL)

	diff = float(sumFL) - float(sumKL)
	diff = diff / (noOfCourse - 1)
	curr_stu = Student.objects.get(user_id=request.session['login_id'])
	dep = CourseDependency.objects.get(course_source_id = curr_stu.prev_course.id, course_target_id = request.session['course_id'])

	dep.average_change = ((float(dep.average_change)*float(dep.total_stu)) + diff)/ (float(dep.total_stu) + 1)
	 
	dep.total_stu = dep.total_stu + 1;
	dep.save()

	if knowledge >= 0.5 : 
		curr_stu.prev_course = Course.objects.get(id = request.session['course_id'])
		curr_stu.save()

	message='Your score is '+str(knowledge*100)+'%. Please <a href="/performance/">click</a> to continue...'	
	return HttpResponse(message)


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
	
	for i in range(15) :
		chosen = request.GET.get(str(i+1))	
		if not chosen:
			messages.error(request, "You can't leave anything blank.")
			return HttpResponseRedirect('/feedback/')
		
	feedback = Feedback(q1=request.GET.get('1'), q2=request.GET.get('2'), q3=request.GET.get('3'), q4=request.GET.get('4'), q5=request.GET.get('5'), q6=request.GET.get('6'), q7=request.GET.get('7'), q8=request.GET.get('8'), q9=request.GET.get('9'), q10=request.GET.get('10'), q11=request.GET.get('11'), q12=request.GET.get('12'), q13=request.GET.get('13'), q14=request.GET.get('14'), q15=request.GET.get('15'))
	feedback.save()
	return HttpResponse('Your response has been saved.Please <a href="/concept_menu/">click</a> to continue...') 
		

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


