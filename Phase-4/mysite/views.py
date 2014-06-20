import time, os, operator

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

from array import *
from decimal import *

from django.db.models import Sum

import datetime

def Evaluation_welcome(request):
    return render (request,'EvaluationWelcome.html')

def Feedback_evaluation(request):

	try :
		r1 =  Feedback.objects.get(id='1')
		numstu = Feedback.objects.latest('id')
		a1 = Feedback.objects.aggregate(Sum('q1'))
		a2 = Feedback.objects.aggregate(Sum('q2'))
		a3 = Feedback.objects.aggregate(Sum('q3'))
		a4 = Feedback.objects.aggregate(Sum('q4'))
		a5 = Feedback.objects.aggregate(Sum('q5'))
		a6 = Feedback.objects.aggregate(Sum('q6'))
		a7 = Feedback.objects.aggregate(Sum('q7'))
		a8 = Feedback.objects.aggregate(Sum('q8'))
		a9 = Feedback.objects.aggregate(Sum('q9'))
		a10 = Feedback.objects.aggregate(Sum('q10'))
		a11 = Feedback.objects.aggregate(Sum('q11'))
		a12 = Feedback.objects.aggregate(Sum('q12'))
		a13 = Feedback.objects.aggregate(Sum('q13'))
		a14 = Feedback.objects.aggregate(Sum('q14'))
		a15 = Feedback.objects.aggregate(Sum('q15'))

		print 'number of students '+ str(numstu)    

		avg1 = cal_avg(a1['q1__sum'],a2['q2__sum'],a3['q3__sum'],numstu.id)    
		avg2 = cal_avg(a4['q4__sum'],a5['q5__sum'],a6['q6__sum'],numstu.id)
		avg3 = cal_avg(a7['q7__sum'],a8['q8__sum'],a9['q9__sum'],numstu.id)
		avg4 = cal_avg(a10['q10__sum'],a11['q11__sum'],a12['q12__sum'],numstu.id)
		avg5 = cal_avg(a13['q13__sum'],a14['q14__sum'],a15['q15__sum'],numstu.id)

		return render(request,'FeedbackEvaluation.html',{'response1':r1, 'ans1':a1, 'ans2':a2, 'ans3':a3, 'ans4':a4, 'ans5':a5, 'ans6':a6, 'ans7':a7, 'ans8':a8, 'ans9':a9, 'ans10':a10, 'ans15':a15, 'ans11':a11, 'ans12':a12, 'ans13':a13, 'ans14':a14, 'mystr':str, 'num_stu':numstu, 'average1':avg1, 'average5':avg5, 'average2':avg2, 'average3':avg3, 'average4':avg4})  

	except:
		message = "No feedbacks found"
		return HttpResponse(message)


def cal_avg(a,b,c,d):
	return (a+b+c)/d

def Material_evaluation(request):

    concept_list = Course.objects.all()                # list of all concepts in the course
    num_concepts = concept_list.count()                # total number of concepts in the model
    concept_correct_questions = []                     # stores number of questions correctly solved in that concept
    concept_total_questions = []                       # stores number of questions attempted in that concept
    mat_list = []
    for i in concept_list:
        temp = []
        temp.append(i.name)
        temp.append(Grade.objects.all().filter(conceptID=Course.objects.get(id=i.id)).aggregate(Sum('value')))
        temp.append(Grade.objects.all().filter(conceptID=Course.objects.get(id=i.id)).count())
        pertemp = (float(temp[1].value__sum*100))/float(temp[2])
        temp.append("{0:.2f}".format(pertemp))
        if pertemp <= 25 :
            temp.append("Poor")
        elif pertemp <= 50 :
            temp.append("Average")
        elif pertemp <= 75 :
            temp.append("Good")
        elif pertemp <= 100 :
            temp.append("Excellent")
        mat_list.append(temp)
    return render (request,'MaterialEvaluation.html',{'num_concepts':num_concepts, 'mat_list':mat_list })  

def Parameter_evaluation(request):

    num_recomendations_displayed = 4
    total_concepts = Course.objects.all().count()

    print 'total concepts in course'
    print total_concepts

    # total number of students who have given ratings to the concepts    

    num_c1_stu = Ratings.objects.filter(item_id=1).count()
    num_c2_stu = Ratings.objects.filter(item_id=2).count()
    num_c3_stu = Ratings.objects.filter(item_id=3).count()
    num_c4_stu = Ratings.objects.filter(item_id=4).count()

    # array to store the number of students who have rated a certain concept

    concept_student_array = array('i',[])

    for j in range(0,total_concepts):
        concept_student_array.insert(j,Ratings.objects.filter(item_id=j+1).count())      

    
    num_good_recommendations = Ratings.objects.filter(rating__gte=4).count()


    # array to store ratings of al concepts
    
    concept_rating_array = array('f',[])

    for i in range(0,total_concepts):
        temp_var = cal_avg_rating(Ratings.objects.filter(item_id=i+1).aggregate(Sum('rating'))['rating__sum'], concept_student_array[i])
        round(temp_var,2)
        print temp_var
        concept_rating_array.insert(i,Decimal(format(temp_var, '.2f')))
    
    # calculate the number of recomendations which are good from total recommendations displayed
    good_recommendation_displayed_count = 0   
    for i in range(0,total_concepts):
        if concept_rating_array[i]>=4 :
           good_recommendation_displayed_count = good_recommendation_displayed_count + 1    

    return render (request,'EvaluationParameters.html',{'num_recomendations_displayed':num_recomendations_displayed, 'num_good_recommendations':num_good_recommendations, 'concept_rating_array':concept_rating_array, 'good_recommendation_displayed_count':good_recommendation_displayed_count})


def cal_avg_rating(a,b):
    if b == 0 :
       return 0
    avg = a/b  
    avg1 = int (avg*100)
    avg2 = avg1/100
    return avg2
 
#changes by sameer end here


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
			grade = Grade(studentID=student,questionID=question,value=0,prev=0,conceptID=question.course, attempted=0)
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

	# calculation student_similarity with other students who have taken this concept.
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
				concept_union = list(set(current_student_concept_list).union(set(other_student_concept_list)))
				concept_common = list(set(current_student_concept_list).intersection(set(other_student_concept_list)))
				if len(concept_common) > 0:
					concept_factor = float(len(concept_common))/len(concept_union)
					average_marks_difference = 0.0
					for concept in concept_common:
						current_student_marks = Student_History.objects.get(student=student,concept=concept).score
						other_student_marks = Student_History.objects.get(student=other_student,concept=concept).score
						if current_student_marks >= other_student_marks:
							average_marks_difference = average_marks_difference + float(current_student_marks - other_student_marks)
						else:
							average_marks_difference = average_marks_difference + float(other_student_marks - current_student_marks)
					average_marks_difference = average_marks_difference/len(concept_common)
					marks_factor = 1.0 - average_marks_difference
					similarity = concept_factor*marks_factor
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
		# Recommend concepts taken by top similar students. but not taken by the current student
		sim1 = Student_Similarity.objects.filter(student1 = student,similarity__gt=0.4)
		sim2 = Student_Similarity.objects.filter(student2 = student,similarity__gt=0.4)
		sim_list = (sim1 | sim2).order_by('-similarity')
		if sim_list:
			concept_limit = 3;
			concept_count = 0;
			for sim in sim_list:
				
				if sim.student1==student:
					other_student = sim.student2
				else:
					other_student = sim.student1
				other_student_history_list = Student_History.objects.filter(student = other_student)
				other_student_concept_list = []
				for history_item in other_student_history_list:
					other_student_concept_list.append(history_item.concept)
				concept_common = list(set(current_student_concept_list).intersection(set(other_student_concept_list)))
				concept_in_other_not_common = list(set(other_student_concept_list) - set(concept_common))
				for concept in concept_in_other_not_common:
					if concept_count>=concept_limit:
						break;
					ss_reco_list.append(concept)
					concept_count = concept_count + 1;
				if concept_count>=concept_limit:
					break;
	student = Student.objects.get(user_id=request.session['login_id'])
	
	attempted_wrongly_grade_list1 = Grade.objects.filter(studentID=student, value=0)
	attempted_wrongly_grade_list = attempted_wrongly_grade_list1.filter(~Q(attempted = 0)) 

	print "Wrongly attempted questions"

	for item in attempted_wrongly_grade_list:
		print item.questionID.id

	concept_list = Course.objects.all()
	num_questions = Question.objects.all().count()
	wrong_concept_importance = []
	num_attempted = 0
	dep_sum = 0
	question_recco = []

	for concept in concept_list:
		num_attempted = 0
		dep_sum = 0
		print "for concept : " + str(concept.name)
		for object1 in attempted_wrongly_grade_list:
			print "for wrongly attempted question, " + str(object1.questionID.id)
			print object1.attempted
			qc = Question_Concept.objects.get(question=object1.questionID, concept=concept)
			if qc.value > 0:
				num_attempted = num_attempted + object1.attempted
				dep_sum = dep_sum + qc.value
		if num_attempted < 0.3*num_questions:
			continue
		importance = 0.5 * float(num_attempted) + 0.5 * float(dep_sum)
		wrong_concept_importance.append((concept,importance))
		print str(num_attempted) + "    " + str(dep_sum) + "     " + str(importance)

	sorted_importance = sorted(wrong_concept_importance, key = operator.itemgetter(1), reverse = True)

	for item in sorted_importance:
		question_recco.append(item[0])	
		print item[0]	

	return render(request, 'concept_menu.html',{'concept_list':clist, 'passed_list':plist, 'student_name' : student.name, 'cf_predict_list' : predict_course_list, 'ss_reco_list':ss_reco_list, 'question_recco':question_recco})

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

	print filename

	MEDIA_DIR = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'), 'media')

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
	
	# Logging the quiz into student_history
	history_found = Student_History.objects.filter(student=student,concept=curr_item)
	if history_found:
		history_object = Student_History.objects.get(student=student,concept=curr_item)
		history_object.score = knowledge
	else: 
		history_object = Student_History(student=student,concept=curr_item,score=knowledge)
	history_object.save()
	if course_id == 1:
		return render(request, 'quiz_result1.html', {'score':score})
	if course_id == 2:
		return render(request, 'quiz_result2.html', {'score':score})
	if course_id == 3:
		return render(request, 'quiz_result3.html', {'score':score})
	if course_id == 4:
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

	item_id = 1
	
	dep_dict = {}
	
	dep_sum = 0

	while item_id >= 0:
		try:
			print "hello " + str(item_id)
			concept_string = "course" + str(item_id)
			print 'course_string' + concept_string
			dependency_string = "dependency" + str(item_id)
			print 'dependency_string' + dependency_string
			concept = int(request.GET.get(concept_string))
			print 'course ' + str(concept)
			dependency = int(request.GET.get(dependency_string))
			print 'dependency' + str(dependency)
			dep_dict.update({concept : dependency})
			dep_sum = dep_sum + dependency
			item_id = item_id + 1
			print "hello " + str(item_id)
		except:
			break	
		
	for key in dep_dict:
		print "hello"
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
			QC_list = Question_Concept.objects.filter(question = question)
			for item in QC_list:
				item.delete()

			QC_new_list = Question_Concept_new.objects.filter(question = question)

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
			
			for item in QC_new_list:
				item.delete()
			
			confidencertor_list = ConfidenceRtoR.objects.filter(Q(questionSource=question) | Q(questionTarget=question))

			for item in confidencertor_list:
				item.delete()

			confidencewtow_list = ConfidenceRtoR.objects.filter(Q(questionSource=question) | Q(questionTarget=question))

			for item in confidencewtow_list:
				item.delete()

			q1q2rightwrong_list = Q1Q2RightWrong.objects.filter(Q(question_x=question) | Q(question_y=question))

			for item in q1q2rightwrong_list:
				item.delete()

			grade_list = Grade.objects.filter(questionID=question)
			
			for item in grade_list:
				item.delete()

			question.delete()
			
	staff_name = User.objects.get(id=request.session['login_id']).username
	return render(request, 'result_staff_question_delete.html',{'staff_name':staff_name, 'save_question' : "1", 'delete_question' : "0"})

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

	if course_id == 1:
		feedback1(request)
	if course_id == 2:
		feedback2(request)
	if course_id == 3:
		feedback3(request)
	if course_id == 4:
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

	concept_list = Course.objects.all()
	for concept in concept_list:
		if concept.name == "Basics of C Programming":
			q = Question(course=concept, question="""C programs are converted 
into machine language with the help of""" , option1="Editor", option2="Compiler", option3="OS", option4="None of the above", answer=2)
			q.save()
			q = Question(course=concept, question="""A character variable can at a time store""" , option1="1 character", option2="8 character", option3="256 characters", option4="None of the above", answer=1)
			q.save()
			q = Question(course=concept, question="""The maximum value that an integer constant can have is""" , option1="-32767", option2="32767", option3="1.7014e+38", option4="depends on the machine", answer=4)
			q.save()
			q = Question(course=concept, question="""Which of the following is not a keyword in C ?""" , option1="for", option2="char", option3="print", option4="case", answer=3)
			q.save()

		elif concept.name == "Decision making":
			q = Question(course=concept, question="""What would be the output of the following program:  main( ) 
		{ 
			int a = 300, b = 0, c = 10 ; 
			if ( a >= 400 ) 
			b = 300 ; 
			c = 200 ; 
			printf ( "\n%d %d", b, c ) ; 		
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
			printf ( "\n%d", k ) ;
			}""", option1="500", option2="30", option3="200", option4="100", answer=3)
			q.save()	
			q = Question(course=concept, question="""What would be the output of the following program:
main( ) 
			{
			int x = 2; 
			if ( x == 2 && x != 0 ) 
				{  
				printf( "\nHello" ) ;  
				} 
			else   
				printf( "Bye" ) ; }""", option1="Hello", option2="Bye", option3="Compilation error", option4="Segmentaion fault", answer=1)
			q.save()	
		elif concept.name == "Iterations":
			q = Question(course=concept, question="""How many times does the for loop iterate?
			for ( i = 0; i< 10 ; i = i+2)""", option1="5", option2="10", option3="6", option4="11", answer=1)
			q.save()
			q = Question(course=concept, question="""In the following code :
			do 
			{
				printf("Hello");
			}
			while ( 4<1);""", option1="hello will be printed", option2="hello will not be printed", option3="depends on compiler", option4="depends on interpreter", answer=2)
			q.save()
			q = Question(course=concept, question="""Output of following code is
                        main( )
                        {  
                        float  x = 11 ;
                        char c = ""a"";
                        while ( x == 11 )  
                                {   
                                        printf ( "\n %d %f",c, x ) ;  
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
			q = Question(course=concept, question="""What will be the output of following code :
{
		int  num[26], temp ;
		num[0] = 100 ;  
		num[25] = 200 ;
		temp = num[25] ;
		num[25] = num[0] ;
		num[0] = temp ;
		printf ( "\n%d %d", num[0], num[25] ) ; }""", option1="100 200", option2="200 100", option3="100 100", option4="200 200", answer=2)
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


