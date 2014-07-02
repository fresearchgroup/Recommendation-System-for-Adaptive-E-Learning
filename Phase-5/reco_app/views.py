import time, os, operator
from django.core.files.base import File as DjangoFile
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from reco_app.models import *
import datetime
from django.shortcuts import render, render_to_response
from reco_app.forms import CourseAddForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Min, Q
from reco_app.tasks import concept_map
from random import *

from array import *
from decimal import *

from django.db.models import Sum

import datetime


def Evaluation_welcome(request):
    if 'logged_in' not in request.session:
        return HttpResponseRedirect("/login-form")
    if request.session['staff_mode'] == 0:
        return HttpResponseRedirect("/concept_menu/")

    return render (request,'EvaluationWelcome.html', {'staff_name':User.objects.get(id=request.session['login_id']).username})

def Feedback_evaluation(request):

	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 0:
		return HttpResponseRedirect("/concept_menu/")

	if 3 == 3 :
		question_list = Feedback_Questions.objects.all()
		num_feedback_questions = question_list.count()
		num_feedback_categories = Feedback_Questions.objects.latest('category')
		mat_list3 = []
		mat_list4 = []
		category_list = ['Effectiveness of system','Adaptivity of system','State on Computer Programming','Students progress in future','Necessity of revision']
		category_list1 = {'1':'Effectiveness of system','2':'Adaptivity of system','3':'State on Computer Programming','4':'Students progress in future','5':'Necessity of revision'}
		for i in question_list :
			temp3 = []
			temp3.append(i.ques)
			sum_responses = Feedback.objects.all().filter(question=i.id).aggregate(Sum('response'))
			num_students = Feedback.objects.all().filter(question=i.id).count()   # number of students who have given response
			if num_students == 0 :
				avg = 0
			else :
				avg = sum_responses['response__sum']/num_students
			
			temp3.append("{0:.2f}".format(avg))

			if avg <= 1.0 :
				temp3.append("Not at all")
				temp3.append("danger")
			elif avg <= 2.0 :
				temp3.append("Somewhat")
				temp3.append("warning")
			elif avg <= 3.0 :
				temp3.append("To some extent")
				temp3.append("warning")
			elif avg <= 4.0 :
				temp3.append("Surely")
				temp3.append("success")
			else :
				temp3.append("Very much")
				temp3.append("success")
			print category_list1[str(i.category)]
			temp3.append(category_list1[str(i.category)])
			mat_list3.append(temp3)
		
		for j in range(0,num_feedback_categories.category):
			temp4 = []
			temp4.append(category_list[j])
			feedback_ques =  Feedback_Questions.objects.filter(category=j+1)
			sum_responses = 0
			num_students = 0
			for ques in feedback_ques:
				agg = Feedback.objects.filter(question = ques).aggregate(Sum('response'))
				if agg['response__sum'] is not None :
					sum_responses = sum_responses + int(agg['response__sum'])
					num_students = num_students + Feedback.objects.filter(question = ques).count()

			if num_students == 0 :
				avg = 0
			else :
				avg = sum_responses/num_students
			
			temp4.append("{0:.2f}".format(avg))
			if avg <= 1.0 :
				temp4.append("Not at all")
				temp4.append("danger")
			elif avg <= 2.0 :
				temp4.append("Somewhat")
				temp4.append("warning")
			elif avg <= 3.0 :
				temp4.append("To some extent")
				temp4.append("warning")
			elif avg <= 4.0 :
				temp4.append("Surely")
				temp4.append("success")
			else :
				temp4.append("Very much")
				temp4.append("success")
			mat_list4.append(temp4)

		return render(request,'FeedbackEvaluation.html',{'mat_list3':mat_list3,'mat_list4':mat_list4})

	else :
		message = "No feedbacks found!"
		return HttpResponse(message)

def cal_avg(a,b,c,d):
	return (a+b+c)/d

def Material_evaluation(request):

    if 'logged_in' not in request.session:
        return HttpResponseRedirect("/login-form")
    if request.session['staff_mode'] == 0:
        return HttpResponseRedirect("/concept_menu/")

    concept_list = Course.objects.all()                # list of all concepts in the course
    num_concepts = concept_list.count()                # total number of concepts in the model
    concept_correct_questions = []                     # stores number of questions correctly solved in that concept
    concept_total_questions = []                       # stores number of questions attempted in that concept
    mat_list = []
    for i in concept_list:
        if i.name == "foundation":
                continue
        temp = []
        temp.append(i.name)
        temp.append(Grade.objects.filter(conceptID=Course.objects.get(id=i.id)).aggregate(Sum('value')))
        if temp[1]['value__sum'] is None:
            temp[1]['value__sum']=0
        temp.append(Grade.objects.filter(conceptID=Course.objects.get(id=i.id)).count())
        if temp[2] == 0:
        	pertemp = 0
        else:
            pertemp = (float(temp[1]['value__sum']*100))/float(temp[2])
            
        temp.append("{0:.2f}".format(pertemp))
        if pertemp <= 25 :
            temp.append("Poor")
            temp.append("danger")
        elif pertemp <= 50 :
            temp.append("Average")
            temp.append("warning")
        elif pertemp <= 75 :
            temp.append("Good")
            temp.append("info")
        elif pertemp <= 100 :
            temp.append("Excellent")
            temp.append("success")
        mat_list.append(temp)
    return render (request,'MaterialEvaluation.html',{'num_concepts':num_concepts, 'mat_list':mat_list, 'staff_name':User.objects.get(id=request.session['login_id']).username })

def Parameter_evaluation(request):

	c_list = Course.objects.all()                # list of all concepts in the course
	total_concepts = len(c_list)
	num_recomendations_displayed = total_concepts - 1;

	concept_student_array = array('i',[])		# array to store the number of students who have rated a certain concept
	concept_rating_array = []
	good_recommendation_displayed_count = 0

	for cor in c_list:
		if cor.name == 'foundation':
			continue
		no_of_stud = Ratings.objects.filter(item = cor).count()
		if no_of_stud > 0 :
			total_rating = Ratings.objects.filter(item = cor).aggregate(Sum('rating'))['rating__sum']
			cor_avg = cal_avg_rating(total_rating, no_of_stud)
		else:
			cor_avg = 0

		temp = []
		temp.append(cor.id)
		temp.append(cor.name)
		temp.append(cor_avg)
		concept_rating_array.append(temp)
		if cor_avg >= 4.0 :
			good_recommendation_displayed_count += 1

	return render (request,'EvaluationParameters.html',{'num_recomendations_displayed':num_recomendations_displayed, 'num_good_recommendations':good_recommendation_displayed_count, 'concept_rating_array':concept_rating_array, 'good_recommendation_displayed_count':good_recommendation_displayed_count})


def cal_avg_rating(a,b):
    if b == 0 :
       return 0
    avg = a/b  
    avg1 = int (avg*100)
    avg2 = avg1/100
    return avg2
 
#Evaluation Pages End


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
			request.session['staff_mode'] = user.is_staff
			if user.is_staff==0: 
				return HttpResponseRedirect("/student_home/")
			else:
				return HttpResponseRedirect("/staff_menu/")
		else:
			message = "Your account has been dsabled!"
	else:
		return render(request, 'login.html', {'error':True})

	return HttpResponse(message)
		

def registeration_form(request):
	return render(request, 'registeration.html', {'error1':False})

def student_home(request):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form/")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")

	return render(request, 'StudentDashboard.html', {'student_name':Student.objects.get(user_id=request.session['login_id']).name})

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
			print "question.id" + str(question.id)
			grade = Grade(studentID=student,questionID=question,value=0,prev=0,conceptID=question.course, attempted=0)
			grade.save()
		
		questionList = Question.objects.all()	
		print "no. of questions in the database : " + str(questionList.count())	
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

		return HttpResponseRedirect('/student_home')

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

	# calculation student_similarity with other students.
	ss_reco_list = []		#student_similarity_recommendation_list
	current_student_history_list = Student_History.objects.filter(student = student)
	if current_student_history_list:
		current_student_concept_list = []
		for history_item in current_student_history_list:
			current_student_concept_list.append(history_item.concept)

		for other_student in Student.objects.all().exclude(id=student.id):
			other_student_history_list = Student_History.objects.filter(student = other_student)
			if other_student_history_list:
				other_student_concept_list = []
				for history_item in other_student_history_list:
					other_student_concept_list.append(history_item.concept)
				concept_common = list(set(current_student_concept_list).intersection(set(other_student_concept_list)))
				if len(concept_common) > 0:
					other_student_score_square_sum = 0.0
					current_student_score_square_sum = 0.0
					common_concept_score_product = 0.0
					for concept in concept_common:
						current_student_marks = Student_History.objects.get(student=student,concept=concept).score
						other_student_marks = Student_History.objects.get(student=other_student,concept=concept).score
						common_concept_score_product += float(current_student_marks)*float(other_student_marks)
					for concept in current_student_concept_list:
						current_student_marks = Student_History.objects.get(student=student,concept=concept).score
						current_student_score_square_sum += float(current_student_marks)**2
					for concept in other_student_concept_list:
						other_student_marks = Student_History.objects.get(student=other_student,concept=concept).score
						other_student_score_square_sum += float(other_student_marks)**2
					similarity = (common_concept_score_product)/((current_student_score_square_sum**(0.5))*(other_student_score_square_sum**(0.5)))

					sim_found_1 = Student_Similarity.objects.filter(student1=student,student2=other_student)
					if sim_found_1:
						sim_found = Student_Similarity.objects.get(student1=student,student2=other_student)
						sim_found.similarity = similarity
						sim_found.save()
					else:
						sim_found_2 = Student_Similarity.objects.filter(student1=other_student,student2=student)
						if sim_found_2:
							sim_found = Student_Similarity.objects.get(student1=other_student,student2=student)
							sim_found.similarity = similarity
							sim_found.save()
						else:
							sim_created = Student_Similarity(student1=student,student2=other_student,similarity=similarity)
							sim_created.save()  
		# Done! Student Similarity stored/updated!
		# Now to show recommended courses of similar students.
		# calculate prediction value for every course not passed by this student.
		all_courses = all_courses.exclude(name="foundation")
		concepts_not_passed = list(set(all_courses)-set(plist))
		sim1 = Student_Similarity.objects.filter(student1 = student,similarity__gt=0.5)
		sim2 = Student_Similarity.objects.filter(student2 = student,similarity__gt=0.5)
		sim_list = (sim1 | sim2).order_by('-similarity')
		if sim_list:
			for concept in concepts_not_passed :
				temp = prediction()
				temp.concept = concept
				temp.prediction_value = 0.0
				prediction_num = 0.0
				prediction_deno = 0.0
				for sim_item in sim_list:
					if sim_item.student1==student:
						other_student = sim_item.student2
					else:
						other_student = sim_item.student1
					other_student_history_list = Student_History.objects.filter(student = other_student)
					other_student_concept_list = []
					for history_item in other_student_history_list:
						other_student_concept_list.append(history_item.concept)
					if concept in other_student_concept_list:
						other_student_score = Student_History.objects.get(student = other_student, concept = concept).score
						prediction_num = prediction_num + float(other_student_score)*float(sim_item.similarity)
						prediction_deno = prediction_deno + float(sim_item.similarity)
				if prediction_deno != 0:
					temp.prediction_value = float(prediction_num)/prediction_deno
				if temp.prediction_value >= 0.5:
					print(temp.prediction_value)
					ss_reco_list.append(temp)
			ss_reco_list.sort(key=lambda prediction:prediction.prediction_value,reverse=True)
		else:
			print("similar students not found.\n")

	student = Student.objects.get(user_id=request.session['login_id'])
	
	attempted_wrongly_grade_list1 = Grade.objects.filter(studentID=student, value=0)
	attempted_wrongly_grade_list = attempted_wrongly_grade_list1.filter(~Q(attempted = 0)) 

	concept_list = Course.objects.all()
	num_questions = 0
	wrong_concept_importance = []
	num_attempted = 0
	dep_sum = 0
	question_recco = []

	for concept in concept_list:
		num_attempted = 0
		dep_sum = 0
		num_questions1 = Question_Concept.objects.filter(concept=concept)
		num_questions = num_questions1.filter(~Q(value = 0))

		for object1 in attempted_wrongly_grade_list:
			qc = Question_Concept.objects.get(question=object1.questionID, concept=concept)
			if qc.value > 0:
				num_attempted = num_attempted + object1.attempted
				dep_sum = dep_sum + qc.value
		if num_attempted < 0.3*(num_questions.count()):
			continue
		importance = 0.5 * float(num_attempted) + 0.5 * float(dep_sum)
		wrong_concept_importance.append((concept,importance))

	sorted_importance = sorted(wrong_concept_importance, key = operator.itemgetter(1), reverse = True)

	for item in sorted_importance:
		question_recco.append(item[0])	

	List = Course.objects.all()

	return render(request, 'concept_menu.html',{'concept_list':clist, 'passed_list':plist, 'student_name' : student.name, 'cf_predict_list' : predict_course_list, 'ss_reco_list':ss_reco_list, 'question_recco':question_recco, 'all':List})

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
	return render(request,'concept_submenu.html',{'student_name' : student_name, 'course_id':course_id})

def pdf_view(request, concept_id):
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")
	request.session['course_id'] = concept_id
	
	filename = str(Course.objects.get(id=request.session['course_id']).content)

	MEDIA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media')

	with open(MEDIA_DIR + '/' + filename,'r') as pdf:
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

def quiz_view(request, concept_id):
		
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")
	request.session['course_id'] = concept_id
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
			gradeObject = Grade(conceptID=question.course,questionID=question, studentID=student, value=0, attempted = 0)

		if chosen == question.answer:
			gradeObject.attempted = 0
			score=score+1
			gradeObject.prev = gradeObject.value
			gradeObject.value=1
		else:
			gradeObject.attempted = gradeObject.attempted + 1
			gradeObject.prev = gradeObject.value
			gradeObject.value=0

		gradeObject.save()

	course_id = int(request.session['course_id'])

	concept_map.delay(course_id, student)

	knowledge = float(score)/num_of_questions
	knowledge = int(knowledge * 100)
	knowledge = float(knowledge)/100

	sumKL = -1
	for studentstate in studentstate_list :
		sumKL = sumKL + float(studentstate.KL)

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
					if float(dependency[0].value) != 0:
						print "dependency : " + str(dependency[0].value)
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

	diff = float(sumFL) - float(sumKL)
	diff = diff / (noOfCourse - 1)
	curr_stu = Student.objects.get(user_id=request.session['login_id'])

	if (curr_stu.prev_course.id != request.session['course_id']) :
		try:
			dep = CourseDependency.objects.get(course_source_id = curr_stu.prev_course.id, course_target_id = request.session['course_id'])
			dep.average_change = ((float(dep.average_change)*float(dep.total_stu)) + diff)/ (float(dep.total_stu) + 1) 
			dep.total_stu = dep.total_stu + 1;
			dep.save()
		except :
			print "same course"

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
			rater_u_avg = float(rater.student.rating_sum)/float(rater.student.rated_concepts)
			rater_u_i = rater.rating
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
	
	# Logging the quiz into student_history
	history_found = Student_History.objects.filter(student=student,concept=curr_item)
	if history_found:
		history_object = Student_History.objects.get(student=student,concept=curr_item)
		history_object.score = knowledge
	else: 
		history_object = Student_History(student=student,concept=curr_item,score=knowledge)
	history_object.save()
	
	num_concepts = Course.objects.all().count()
	num_feedback_questions = Feedback_Questions.objects.all().count()
	to_be_displayed = num_feedback_questions/num_concepts
	
	if to_be_displayed == 0:
		to_be_displayed = 1
	
	starting = int(request.session['course_id']) - int(Course.objects.aggregate(Min('id'))['id__min'])
	ending = starting + to_be_displayed

	ids = []
	feedback_questions = Feedback_Questions.objects.all()
	for item in feedback_questions:
		ids.append(item.id) 

	if to_be_displayed > len(feedback_questions):
		to_be_displayed = len(feedback_questions)
	list1 = sample(ids,to_be_displayed)
	ques = []
	for item in list1:
		ques.append(Feedback_Questions.objects.get(id = item))

	return render(request, 'quiz_result.html', {'score':score, 'question_list':ques})

def all_feedback_view(request):
	student_name = Student.objects.get(user_id=request.session['login_id']).name
	question_list = Feedback_Questions.objects.all()
	return render(request, 'feedback.html', {'student_name':student_name, 'question_list':question_list})

def feedback_handler(request) :
	if 'logged_in' not in request.session:
		return HttpResponseRedirect("/login-form")
	if request.session['staff_mode'] == 1:
		return HttpResponseRedirect("/staff_menu/")

	student = Student.objects.get(user_id=request.session['login_id'])
	feedback = []

	for item in request.GET:
		feedback.append(Feedback(student = student, question = Feedback_Questions.objects.get(id = item), response = request.GET[item]))

	for item in feedback:
		item.save()
	
	return HttpResponse("Thank you for your feedback! Click <a href = '/concept_menu/'>here</a> to continue")
		

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
		form = CourseAddForm(request.POST, request.FILES)
		if request.FILES:	
			if request.POST.get('filename') != "":
				instance = Course(name=request.POST.get('filename'), content=request.FILES['myfile'])		
				instance.save()
				return HttpResponse('Your file has been saved.Please <a href="/staff_menu/">click</a> to continue...')
			else:
				form = CourseAddForm()	
				messages.error(request, "You haven't provided a name...")		
		else:
			form = CourseAddForm()	
			messages.error(request, "You haven't selected anything...")		
	else:
		form = CourseAddForm()
	staff_name = User.objects.get(id=request.session['login_id']).username
	return render(request, 'add_course.html', {'form':form,'staff_name':staff_name})

def concept_upload_handler(request):  
	return HttpResponse("under construction")

def delete_concept_view(request):
	concept_list = Course.objects.all()
	staff_name = User.objects.get(id=request.session['login_id']).username
	return render(request, 'concept_delete.html', {'concept_list':concept_list,'staff_name':staff_name})

def concept_deletion_handler(request):
	concept_list = Course.objects.all()
	for concept in concept_list:
		if request.GET.get(str(concept.id)):
			path = os.path.join(os.path.join(os.path.realpath(os.path.dirname(__file__)),'media'),str(concept.content))
			os.remove(path)
			concept.delete()		
			
	return HttpResponse("Your concept has been deleted")

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
	q.save() #question is saved

	# Now, for consistency the grade for all the students in that question is 0
	student_list = Student.objects.all()
	for student in student_list:
		g = Grade(conceptID=course,questionID=q,studentID=student,value=0,prev=0,attempted=0)
		g.save()

	# We change the Q1Q2RightWrong table too. no. of students right in oth questions is 0 and no. of students wrong in both questions is the number of students wrong in the question which existed previously in the database.
	question_list = Question.objects.all()
	for item in question_list:
		if item is q:
			object1 = Q1Q2RightWrong(question_x = item, question_y = item, right = 0, wrong = Student.objects.all().count())
			object1.save()
		else:
			object1 = Q1Q2RightWrong(question_x = q, question_y = item, right = 0, wrong = len(Grade.objects.filter(questionID=item, value=0)))
			object1.save()

	item_id = 1
	
	dep_dict = {}
	
	dep_sum = 0

	# Here, we retrieve the dependency between questions and concepts
	while item_id >= 0:
		try:
			concept_string = "course" + str(item_id)
			dependency_string = "dependency" + str(item_id)
			concept = int(request.GET.get(concept_string))
			dependency = int(request.GET.get(dependency_string))
			dep_dict.update({concept : dependency})
			dep_sum = dep_sum + dependency
			item_id = item_id + 1
		except:
			break	
		
	# Here, we store those values in question concept matrix
	for key in dep_dict:
		concept = Course.objects.get(id=key)
		value = float(dep_dict[key])/float(dep_sum)
		try:
			qc = Question_Concept.objects.get(question=q,concept=concept)
			qc.value = value
			qc.save()
		except:
			qc = Question_Concept(question=q,concept=concept,value=value)
			qc.save()
	
	concept_list = Course.objects.all()
	for item in concept_list:
		try:
			qc = Question_Concept.objects.get(question=q, concept=item)
		except:
			qc = Question_Concept(question=q, concept=item, value=0)
			qc.save()

	
	# We calculate the QC' matrix on the basis of QC matrix
	for key in dep_dict:
		concept = Course.objects.get(id=key)
		vertical_column = Question_Concept.objects.filter(concept=concept)
		sum1 = 0
		for item2 in vertical_column:
			sum1 += item2.value
		
		for item2 in vertical_column:
			value = item2.value
			if sum1 > value:
				value = float(item2.value)/float(sum1)
			else:
				value = item2.value
			
			try:
				object1 = Question_Concept_new.objects.get(question=item2.question, concept=concept)
				object1.value = value
				object1.save()
			except:
				object1 = Question_Concept_new(question=item2.question, concept=concept, value=value)
				object1.save()

	# Filling out the other values, whose dependency wasn't mentioned
	for item in concept_list:
		try:
			object1 = Question_Concept_new.objects.get(question=q, concept=item)
		except:
			object1 = Question_Concept_new(question=q, concept=item, value=0)
			object1.save()

	staff_name = User.objects.get(id=request.session['login_id']).username
	return render(request, 'result_staff_question_added.html',{'staff_name':staff_name, 'save_question' : "0", 'delete_question' : "1"})
			
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
			# We delete that question's item from QC matrix table
			QC_list = Question_Concept.objects.filter(question = question)
			for item in QC_list:
				item.delete()

			# Retrieve the related items from QC' matrix
			QC_new_list = Question_Concept_new.objects.filter(question = question)

			# Change the values in vertical column
			for item in QC_new_list:
				if item.value > 0:
					vertical_column = Question_Concept.objects.filter(concept = item.concept)
					sum1 = 0
					value = 0
					for item2 in vertical_column:
						sum1 = sum1 + item2.value
	
					for item2 in vertical_column:
						if sum1 > item2.value:
							value = float(item2.value)/float(sum1)
						else:
							value = item2.value
						try:
							object1 = Question_Concept_new.objects.get(question=item2.question, concept=item2.concept)
							object1.value = value
							object1.save()
						except:
							object1 = Question_Concept_new(question=item2.question, concept=item2.concept, value=value)
							object1.save()
			
			# delete the items
			for item in QC_new_list:
				item.delete()
			
			confidencertor_list = ConfidenceRtoR.objects.filter(Q(questionSource=question) | Q(questionTarget=question))

			# delete from confidence_R_to_R matrix
			for item in confidencertor_list:
				item.delete()

			confidencewtow_list = ConfidenceRtoR.objects.filter(Q(questionSource=question) | Q(questionTarget=question))

			# delete from confidence_W_to_W matrix
			for item in confidencewtow_list:
				item.delete()

			q1q2rightwrong_list = Q1Q2RightWrong.objects.filter(Q(question_x=question) | Q(question_y=question))

			# delete from Q1Q2RightWrong matrix
			for item in q1q2rightwrong_list:
				item.delete()

			grade_list = Grade.objects.filter(questionID=question)

			# delete from Grade table
			for item in grade_list:
				item.delete()

			# finally delte the question
			question.delete()
			
	staff_name = User.objects.get(id=request.session['login_id']).username
	return render(request, 'result_staff_question_delete.html',{'staff_name':staff_name, 'save_question' : "1", 'delete_question' : "0"})

def add_stuff(request):

	concept_list = Course.objects.all()

	for concept in concept_list:
		path = os.path.join(os.path.join(os.path.realpath(os.path.dirname(__file__)),'media'),str(concept.content))
		print path
		try:
			os.remove(path)
		except OSError:
			print "OSError"
		concept.delete()

	List = Q1Q2RightWrong.objects.all()
	for item in List:
		item.delete()

	List = Question_Concept.objects.all()
	for item in List:
		item.delete()

	List = Question_Concept_new.objects.all()
	for item in List:
		item.delete()

	List = Grade.objects.all()
	for item in List:
		item.delete()

	List = ConfidenceRtoR.objects.all()
	for item in List:
		item.delete()


	List = ConfidenceWtoW.objects.all()
	for item in List:
		item.delete()

	List = Question.objects.all()
	for item in List:
		item.delete()

	List = Feedback.objects.all()
	for item in List:
		item.delete()

	List = Feedback_Questions.objects.all()
	for item in List:
		item.delete()	

	
	name = "foundation"
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	path = os.path.join(os.path.join(os.path.join(os.path.join(SITE_ROOT,'..'),'media'),'documents'),'dummy')
	new_file = Course(name=name)
	new_file.content = DjangoFile(file(path))
	new_file.save()

	name = "Basics of C Programming"
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	path = os.path.join(os.path.join(os.path.join(os.path.join(SITE_ROOT,'..'),'media'),'documents'),'part_1.pdf')
	new_file = Course(name=name)
	new_file.content = DjangoFile(file(path))
	new_file.save()

	name = "Decision making"
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	path = os.path.join(os.path.join(os.path.join(os.path.join(SITE_ROOT,'..'),'media'),'documents'),'part_2.pdf')
	new_file = Course(name=name)
	new_file.content = DjangoFile(file(path))
	new_file.save()

	name = "Iterations"
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	path = os.path.join(os.path.join(os.path.join(os.path.join(SITE_ROOT,'..'),'media'),'documents'),'part_3.pdf')
	new_file = Course(name=name)
	new_file.content = DjangoFile(file(path))
	new_file.save()

	name = "Arrays and Structures"
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	path = os.path.join(os.path.join(os.path.join(os.path.join(SITE_ROOT,'..'),'media'),'documents'),'part_4.pdf')
	new_file = Course(name=name)
	new_file.content = DjangoFile(file(path))
	new_file.save()
	
	name = "Multi-dimensional Arrays"
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	path = os.path.join(os.path.join(os.path.join(os.path.join(SITE_ROOT,'..'),'media'),'documents'),'part_8.pdf')
	new_file = Course(name=name)
	new_file.content = DjangoFile(file(path))
	new_file.save()

	name = "Pointers"
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	path = os.path.join(os.path.join(os.path.join(os.path.join(SITE_ROOT,'..'),'media'),'documents'),'part_5.pdf')
	new_file = Course(name=name)
	new_file.content = DjangoFile(file(path))
	new_file.save()

	name = "Functions"
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	path = os.path.join(os.path.join(os.path.join(os.path.join(SITE_ROOT,'..'),'media'),'documents'),'part_6.pdf')
	new_file = Course(name=name)
	new_file.content = DjangoFile(file(path))
	new_file.save()

	name = "File Handling"
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	path = os.path.join(os.path.join(os.path.join(os.path.join(SITE_ROOT,'..'),'media'),'documents'),'part_7.pdf')
	new_file = Course(name=name)
	new_file.content = DjangoFile(file(path))
	new_file.save()

	concept_list = Course.objects.all()
	for concept in concept_list:
		print concept.name
		if concept.name == "Basics of C Programming":
			print concept.name
			q = Question(course=concept, question="""C programs are converted into machine language with the help of""" , option1="Editor", option2="Compiler", option3="OS", option4="None of the above", answer=2)
			q.save()
			q = Question(course=concept, question="""A character variable can at a time store""" , option1="1 character", option2="8 character", option3="256 characters", option4="None of the above", answer=1)
			q.save()
			q = Question(course=concept, question="""The maximum value that an integer constant can have is""" , option1="-32767", option2="32767", option3="1.7014e+38", option4="depends on the machine", answer=4)
			q.save()
			q = Question(course=concept, question="""Which of the following is not a keyword in C ?""" , option1="for", option2="char", option3="print", option4="case", answer=3)
			q.save()

		elif concept.name == "Multi-dimensional Arrays":
			print concept.name
			q = Question(course=concept, question="""int a[10][20]; 
which is true for a: """ , option1="a is true two-dimensional array", option2="200 int-sized locations have been set aside", option3="Conventional rectangular subscript calculation 20*row+col is used to find element a[row,col]", option4="All of the mentioned", answer=4)
			q.save()
			q = Question(course=concept, question="""int *b[10]; 
which is true for b""" , option1="The definition only allocates 10 pointers and does not initialize them", option2="Initialization must be done explicitly", option3="Both a and b", option4="Error", answer=3)
			q.save()
			q = Question(course=concept, question="""What is the output of this C code?
#include <stdio.h>
void main()
{
    char a[10][5] = {"hi", "hello", "fellows"};
    printf("%s", a[2]);
}""" , option1="fellows", option2="fellow", option3="fello", option4="fell", answer=3)
			q.save()
			q = Question(course=concept, question="""What is the output of the following code?
#include <stdio.h>
void main()
{
	int i,j,a[3][3]={{1,2,3},{4,5,6},{7,8,9}};
	for(i=0;i<5;i++)
		for(j=0;j<5;j++)
			if ((i*j)%2 = 0)
				printf("%d",a[i][j]);
}""" , option1="123456789", option2="12346789", option3="13456789", option4="12345679", answer=2)
			q.save()

		elif concept.name == "File Handling":
			print concept.name
			q = Question(course=concept, question="""The first and second arguments of fopen are : """ , option1="A character string containing the name of the file & the second argument is the mode.", option2=" A character string containing the name of the user & the second argument is the mode.", option3="A character string containing file poniter & the second argument is the mode.", option4="None of the above", answer=1)
			q.save()
			q = Question(course=concept, question="""For binary files, a ___ must be appended to the mode string.""" , option1="Nothing", option2="b", option3="binary", option4="01", answer=2)
			q.save()
			q = Question(course=concept, question="""If there is any error while opening a file, fopen will return : """ , option1="Nothing", option2="EOF", option3="NULL", option4="depends on compiler", answer=3)
			q.save()
			q = Question(course=concept, question="""FILE is of type ______ ?""" , option1="int type", option2="char * type", option3="struct type", option4="none of the mentioned", answer=3)
			q.save()
			q = Question(course=concept, question="""What is the meant by a in the following operation?
fp = fopen(Random.txt, a);""" , option1="attach", option2="append", option3="apprehend", option4="add", answer=2)
			q.save()
			q = Question(course=concept, question="""Which of the following mode argument is used to truncate?""" , option1="a", option2="f", option3="w", option4="t", answer=3)
			q.save()
			q = Question(course=concept, question="""Which type of file cannot be opened using fopen() in C?""" , option1=".txt", option2=".bin", option3=".c", option4="none of the above", answer=4)
			q.save()

		elif concept.name == "Functions":
			print concept.name
			q = Question(course=concept, question="""Correct syntax of  addition function definition in C  is :""" , option1="""
addition int (int a, int b)
{

}""", option2="""
int addition (int a, int b)
{

}""", option3="""
int addition (a : int, b : int)
{

}""", option4="""
addition ( a:int , b:int ) int:
{

}""", answer=2)
			q.save()
			q = Question(course=concept, question="""The number of expressions that can be included in the return statement is :""" , option1="1", option2="2", option3="3", option4="can be many", answer=1)
			q.save()
			q = Question(course=concept, question="""In call by reference to a function, """ , option1="Value of actual and formal parameters change", option2="Value of actual parameter changes", option3="value of formal parameter changes", option4="Value of actual and formal parameters do not change", answer=3)
			q.save()
			q = Question(course=concept, question="""If the following function is called repeatedly 3 times, the output will be :				
display_number()
{
	static int number = 2;
	printf("number = %d", number);
	number ++;
}""" , option1="2 2 2", option2="2 3 4", option3="2 4 6", option4="2 3 3", answer=2)
			q.save()

		elif concept.name == "Pointers":
			print concept.name
			q = Question(course=concept, question="""Output of the following program is :
#include <stdio.h>
const int MAX = 3 ;
int main ()
{
	int var[] = { 100 , 120 , 200 };
	int i, *ptr;
	ptr = var;

	printf("Value of var[0] = %d\n", *ptr );
	return 0;
}
""" , option1="120", option2="100", option3="200", option4="garbage value", answer=2)
			q.save()
			q = Question(course=concept, question="""When a pointer variable is created, its value is initialized by default to :""" , option1="zero", option2="null", option3="grabage value", option4="not set to any value", answer=4)
			q.save()
			q = Question(course=concept, question="""When a pointer is passed to a function, the changes to it in the function are :""" , option1="temporary i.e. not effective outside the scope of the function", option2="permanent i.e. value is changed globally", option3="changes cannot be made to the value of the pointer", option4="none of the above", answer=2)
			q.save()
			q = Question(course=concept, question="""A pointer to variable 'a' points to  :""" , option1="value of 'a'", option2="address of 'a'", option3="datatype of 'a'", option4="none of the above", answer=2)
			q.save()

		elif concept.name == "Decision making":
			print concept.name
			q = Question(course=concept, question="""What would be the output of the following program:  
main( ) 
{ 
	int a = 300, b = 0, c = 10 ; 
	if ( a >= 400 ) 
		b = 300 ; 
	c = 200 ; 
	printf ( "\\n%d %d", b, c ) ; 		
}""", option1="0 10", option2="10 0", option3="0 200", option4="200 300", answer=3)
			q.save()	
			q = Question(course=concept, question="""What would be the output of the following program:
main( ) 
{ 
	int   x = 10, y = 20 ; 
	x == 20 && y != 10 ? printf( "True" ) : printf( "False" ) ; 
}""", option1="true", option2="false", option3="compilation error", option4="none of the above", answer=2)
			q.save()	
			q = Question(course=concept, question="""What would be the output of the following program:
main( ) 
{  
	int   k, num = 30 ;  
	k = ( num > 5 ? ( num <= 10 ? 100 : 200 ) : 500 ) ;  
	printf ( "\\n%d", k ) ;
}""", option1="500", option2="30", option3="200", option4="100", answer=3)
			q.save()	
			q = Question(course=concept, question="""What would be the output of the following program:
main( ) 
{
	int x = 2; 
	if ( x == 2 && x != 0 ) 
	{  
		printf( "\\nHello" ) ;  
	} 
	else   
		printf( "Bye" ) ; 
}""", option1="Hello", option2="Bye", option3="Compilation error", option4="Segmentaion fault", answer=1)
			q.save()	
		elif concept.name == "Iterations":
			print concept.name
			q = Question(course=concept, question="""How many times does the for loop iterate?
for ( i = 0; i< 10 ; i = i+2)
{

}""", option1="5", option2="10", option3="6", option4="11", answer=1)
			q.save()
			q = Question(course=concept, question="""In the following code :
do 
{
	printf("Hello");
}while ( 4<1);""", option1="hello will be printed", option2="hello will not be printed", option3="depends on compiler", option4="depends on interpreter", answer=2)
			q.save()
			q = Question(course=concept, question="""Output of following code is
main( )
{  
	float  x = 11 ;
	char c = ""a"";
	while ( x == 11 )  
    {   
    	printf ( "\\n %d %f",c, x ) ;  
    	x = x - 1 ; 
    }
}
""", option1="datatype mismatch error", option2="97 11.00", option3="65 1.10", option4="65 1.00", answer=2)
			q.save()
			q = Question(course=concept, question="""The value of variable " count" after the outer for loop is :	
int count = 0;	
for ( i = 0; i < 5 ; i++)
	for ( j = 0; j<10; j++)
		count++;""", option1="5", option2="10", option3="50", option4="100", answer=3)
			q.save()
		elif concept.name == "Arrays and Structures":
			print concept.name
			q = Question(course=concept, question="""What will be the output of following code :
{
	int  num[26], temp ;
	num[0] = 100 ;  
	num[25] = 200 ;
	temp = num[25] ;
	num[25] = num[0] ;
	num[0] = temp ;
	printf ( "\\n%d %d", num[0], num[25] ) ; 
}""", option1="100 200", option2="200 100", option3="100 100", option4="200 200", answer=2)
			q.save()
			q = Question(course=concept, question="""What is the starting index of an array?""", option1="1", option2="2", option3="3", option4="0", answer=4)
			q.save()
			q = Question(course=concept, question="""When an array is passed from main function to other function through call by reference, if the values of array elements in the function change, then the values in main """, option1="change", option2="do not change", option3="change only in the case of call by value", option4="none of the above", answer=1)
			q.save()
			q = Question(course=concept, question="""The memory locations of consecutive elements in array are :""", option1="consecutive", option2="differ by 2", option3="differ by 6", option4="differ by 8", answer=2)
			q.save()



	wrong = Student.objects.all().count()
	question_list = Question.objects.all()
	num_questions = question_list.count()
	
	i = 0
	while i < num_questions:
		j = i + 1
		while j < num_questions:
			if question_list[i] == question_list[j]:
				j = j + 1
				continue
			object1 = Q1Q2RightWrong(question_x=question_list[i],question_y=question_list[j],right=0,wrong=wrong)
			object1.save()
			j = j + 1
		i = i + 1

	for question in question_list:
		object1 = Q1Q2RightWrong(question_x=question, question_y=question, right=0, wrong=wrong)
		object1.save()





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

	fq = []
	fq.append(Feedback_Questions(ques="Does the educational software meet your expectations ?", category=1))
	fq.append(Feedback_Questions(ques="Does the educational software help you understanding the logic of programming ?", category=1))
	fq.append(Feedback_Questions(ques="Do you think that this educational software is useful as an educational tool ?", category=1))
	fq.append(Feedback_Questions(ques="Does the program correspond to your knowledge level each time ?", category=2))
	fq.append(Feedback_Questions(ques="Does the program correspond to your educational needs level each time ?", category=2))
	fq.append(Feedback_Questions(ques="Does the test adapt to your educational needs ?", category=2))
	fq.append(Feedback_Questions(ques="Does the educational software affect positively your perception about computer programming ?", category=3))
	fq.append(Feedback_Questions(ques="Does the educational software draw your interest on computer programming ?", category=3))
	fq.append(Feedback_Questions(ques="Does the educational software motivate you to be involved in computer programming ?", category=3))
	fq.append(Feedback_Questions(ques="Does the educational software help you understanding better the logic of programming ?", category=4))
	fq.append(Feedback_Questions(ques="Does the educational software help you to learn other programming languages ?", category=4))
	fq.append(Feedback_Questions(ques="Does the educational software help you in your studies ?", category=4))
	fq.append(Feedback_Questions(ques="Do you think that your returns to a previous chapter in order to revise it are a waste of time ?", category=5))
	fq.append(Feedback_Questions(ques="Do the returns to a previous chapter correspond to your need for revision ?", category=5))
	fq.append(Feedback_Questions(ques="Does your return to a previous level, that happened each time the system discovered that you made errors of previous chapters,help you learning programming ?", category=5))
	
	for ff in fq:
		ff.save()

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
    
