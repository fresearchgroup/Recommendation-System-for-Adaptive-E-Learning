from __future__ import absolute_import
from celery import task
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reco_app.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import datetime
from django.shortcuts import render, render_to_response
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Min, Q

@task
def concept_map(course_id, student):
#	print "hello"
# This is step 1 and step 2 combined.
#This is where the concept mapping starts
# STEP 1:
	# In this step, we check the eligibilty of question pairs, whose relationship matters, greater than cutoff, which is "no of student * 40%"
# STEP 2:
# we have got the pair of question which are eligible for the algoithm to be applied
	# In this step, we will obtain confidence between two questions.
	# confidence(Q_x ----> Q_y) = Support(Q_x, Q_y) / Support(Q_x)
	# Support for questions means that how many responses were right/wrong for those.
	# As such, we get four confidence, one in which support was for rightly attempted questions and another one in which support was for wrongly attempted questions. Rest of the two are just the opposite pairs i.e. Q_y ----> Q_x

#	list_confidence_r_to_r = ConfidenceRtoR.objects.filter()
#	list_confidence_w_to_w = ConfidenceWtoW.objects.all()
	
#	for object1 in list_confidence_r_to_r:
		#print "deleting1"
#		object1.delete()
#	for object2 in list_confidence_w_to_w:
		#print "deleting2"				
#		object2.delete()

	#print "course_id = " + course_id

	questionList_attempted = Question.objects.filter(course_id = course_id)
	questionList = Question.objects.all()
	cutoff = Student.objects.all().count() * 0.4
	lengthOfQuestionList = len(questionList)
	
#	print "no. of questions attempted : " + str(len(questionList_attempted))	
	

	

	for question1 in questionList_attempted:
		object1 = Grade.objects.get(questionID=question1,studentID=student)
		prev1 = object1.prev
		change1 = object1.value - object1.prev	   # 1 for wrong to right
												   # -1 for right to wrong
												   # 0 for no change
		
	#	print "question1 = " + str(question1.id)

		List = Q1Q2RightWrong.objects.filter(Q(question_x=question1)|Q(question_y=question1))
	#	print len(List)
		#print "length of the list: " + str(len(List))	
	
		for object3 in List:
			#print "1"			
			question2 = object3.question_y
			if question1.id == question2.id:
				question2 = object3.question_x
			if question2 in questionList_attempted:
				continue
	#		print "question2 = " + str(question2.id) + " object3.id = " + str(object3.id)

			object2 = Grade.objects.get(questionID=question2,studentID=student)
			prev2 = object2.prev
			change2 = object2.value - object2.prev # 1 for wrong to right
												   # -1 for right to wrong
												   # 0 for no change

			if change1 == 0 and change2 == 0:
				continue

			if change1 == 1:
				if prev2 == 0:
					object3.wrong = object3.wrong - 1
				#	print "changing"
				if prev2 + change2 == 1:
					object3.right = object3.right + 1
				#	print "changing"
			elif change1 == -1:
				if prev2 + change2 == 0:
					object3.wrong = object3.wrong + 1
				#	print "changing"
				if prev2 == 1:
					object3.right = object3.right - 1
				#	print "changing"
						
			object3.save()
	
	i = 0
	length = len(questionList_attempted)
	while i < length:
		j = i
		question1 = questionList_attempted[i]
		object1 = Grade.objects.get(questionID=question1,studentID=student)
		prev1 = object1.prev
		change1 = object1.value - object1.prev
		#print "question1 = " + str(question1.id)
		while j < length:
			question2 = questionList_attempted[j]
			object3 = Q1Q2RightWrong.objects.get(question_x=question1,question_y=question2)
			object2 = Grade.objects.get(questionID=question2,studentID=student)
			prev2 = object2.prev
			change2 = object2.value - object2.prev # 1 for wrong to right
												   # -1 for right to wrong
												   # 0 for no change
	#		print "question2 = " + str(question2.id)

			if change1 == 0 and change2 == 0:
				j = j + 1
				continue

			if change1 == 1:
				if prev2 == 0:
					object3.wrong = object3.wrong - 1
				#	print "changing"
				if prev2 + change2 == 1:
					object3.right = object3.right + 1
				#	print "changing"
			elif change1 == -1:
				if prev2 + change2 == 0:
					object3.wrong = object3.wrong + 1
				#	print "changing"
				if prev2 == 1:
					object3.right = object3.right - 1
				#	print "changing"
						
			object3.save()
			j = j + 1
		i = i + 1
		

	for question1 in questionList_attempted:

		#print "testing time start"			

		List = Q1Q2RightWrong.objects.filter(question_x=question1)
		scoreSourceRight = Q1Q2RightWrong.objects.get(question_x=question1, question_y=question1).right
		scoreSourceWrong = Q1Q2RightWrong.objects.get(question_x=question1, question_y=question1).wrong

		#print "testing time end"

		#print "in loop second question1 : " + str(question1.id)
		for object3 in List:
			#print "testing time start"			
			question2 = object3.question_y
			if question1.id == question2.id:
				question2 = object3.question_x
				if question1.id == question2.id:
					continue
			
			scoreRight = object3.right
			scoreWrong = object3.wrong

			xnor = scoreRight + scoreWrong
			if xnor < cutoff:
				continue
			object4 = Q1Q2RightWrong.objects.get(question_x=question2, question_y=question2)

			scoreTargetRight = object4.right
			scoreTargetWrong = object4.wrong
			
			if scoreRight == 0:
				scoreSourceRight = 1
				scoreTargetRight = 1
			if scoreWrong == 0:
				scoreSourceWrong = 1
				scoreTargetWrong = 1

	#		print "----------------------------"
	#		print "Q1 = " + str(question1.id)
	#		print "Q2 = " + str(question2.id)


	#		print "scoreRight = " + str(scoreRight)
	#		print "scoreWrong = " + str(scoreWrong)
	#		print "scoreSourceRight = " + str(scoreSourceRight)
	#		print "scoreSourceWrong = " + str(scoreSourceWrong)
	#		print "scoreTargetRight = " + str(scoreTargetRight)
	#		print "scoreTargetWrong = " + str(scoreTargetWrong)
			
			#print "testing time end1"
			value1 = float(scoreRight)/float(scoreSourceRight)
			try:
				instance1 = ConfidenceRtoR.objects.get(questionSource=question1, questionTarget=question2)
				instance1.confidenceValue = value1
				if value1 >= 0.75:
					instance1.save()
				else:
					instance1.delete()
			except:
				if value1 >= 0.75:
					instance1 = ConfidenceRtoR(questionSource=question1, questionTarget=question2, confidenceValue=value1)
					instance1.save()

			value2 = float(scoreRight)/float(scoreTargetRight)
			try:
				instance2 = ConfidenceRtoR.objects.get(questionSource=question2, questionTarget=question1)
				instance2.confidenceValue = value2
				if value2 >= 0.75:
					instance2.save()
				else:
					instance2.delete()
			except:
				if value2 >= 0.75:
					instance2 = ConfidenceRtoR(questionSource=question2, questionTarget=question1, confidenceValue=value2)
					instance2.save()
			value3 = float(scoreWrong)/float(scoreSourceWrong)
			try:
				instance3 = ConfidenceWtoW.objects.get(questionSource=question1, questionTarget=question2)
				instance3.confidenceValue = value3
				if value3 >= 0.75:
					instance3.save()	
				else:
					instance3.delete()
			except:
				if value3 >= 0.75:
					instance3 = ConfidenceWtoW(questionSource=question1, questionTarget=question2, confidenceValue=value3)
					instance3.save()
			value4 = float(scoreWrong)/float(scoreTargetWrong)
			try:
				instance4 = ConfidenceWtoW.objects.get(questionSource=question2, questionTarget=question1)
				instance4.confidenceValue = value4
				if value4 >= 0.75:
					instnce4.save()
				else:
					instance4.delete()
			except:
				if value4 >= 0.75:
					instance4 = ConfidenceWtoW(questionSource=question2, questionTarget=question1, confidenceValue=value4)
					instance4.save()
			#print "saved..."				

			#print "testing time end2"

			
	#	print "----------------------------"

# All other steps are combined as follows. Currently step 3 has not been implemented.
	
# STEP 3:

# Here I am supposed to calculate the Question Concept matrix again fromm the original one. QC'. Rules are:
# 	CASE 1 : if two or more non zero values in column C_t of the original questions-concept matrix QC, then new element is the fraction of what that question contributes to that concept with respect to the contribution of all the other questions.

#	CASE 2 : if just one non-zero element, then take that only.


# STEP 4:

# Here, we actually calculate the relevence between two concepts. formula is : 
#	rev(C_i, C_j)_(Q_x ----> Q_y) = qc_(xi) * qc_(yj)' * confidence(Q_x ----> Q_y)
	

# STEP 5:

# calculate u = min of every element of the QC matrix 
# if rev (calculated in step 4) < u, then calculate e_(ij) = N_i + N_j
# N_i : no of questions for concept i
# N_j : no of questions for concept j
# if e_(ij) < no of questions * 0.5, then preserve the relevence even if it is less than u.

# STEP 6:

# If all conditions are met and the associative rule is correctly learned to correctly learned, then it is concept2 to concept1
# If all conditions are met and the associative rule is incorrectly learned to incorrectly learned, then it is concept1 to concept2


# STEP 7:

# there are multiple relevence values, choose the maximum one.
	min_value = Question_Concept.objects.all().aggregate(Min('value'))['value__min']
	m = Question.objects.count() # no. of questions
	concept_list = Course.objects.all()
	length = len(concept_list)
	i = 0
	
	while i < length:
		concept1 = concept_list[i]
		n1 = Question_Concept.objects.filter(concept=concept1).count()
		j = i + 1
		while j < length:
			concept2 = concept_list[j]
			if concept1 is concept2:
				j = j + 1
				continue
			n2 = Question_Concept.objects.filter(concept=concept2).count()
			rev_1to2 = 0
			rev_2to1 = 0
			dependency_list_right = ConfidenceRtoR.objects.all()
			for item in dependency_list_right:
				question_source = item.questionSource
				question_target = item.questionTarget
				
				confidence = item.confidenceValue
				qc_source_1 = Question_Concept.objects.get(question=question_source, concept=concept1)
				qc_target_2 = Question_Concept.objects.get(question=question_target, concept=concept2)				
				qc_source_2 = Question_Concept.objects.get(question=question_source, concept=concept2)
				qc_target_1 = Question_Concept.objects.get(question=question_target, concept=concept1)
				
				rev2to1 = qc_source_1.value * qc_target_2.value * confidence
				rev1to2 = qc_source_2.value * qc_target_1.value * confidence
		
				if rev2to1 >= min_value or ((n1+n2) < (m * 0.5)):
					if rev2to1 > rev_2to1:
						rev_2to1 = rev2to1
				if rev1to2 >= min_value or ((n1+n2) < (m * 0.5)):
					if rev1to2 > rev_1to2:
						rev_1to2 = rev1to2				
				
			dependency_list_wrong = ConfidenceWtoW.objects.all()
			for item in dependency_list_wrong:
				question_source = item.questionSource
				question_target = item.questionTarget
				
				confidence = item.confidenceValue
				qc_source_1 = Question_Concept.objects.get(question=question_source, concept=concept1)
				qc_target_2 = Question_Concept.objects.get(question=question_target, concept=concept2)				
				qc_source_2 = Question_Concept.objects.get(question=question_source, concept=concept2)
				qc_target_1 = Question_Concept.objects.get(question=question_target, concept=concept1)
				
				rev1to2 = qc_source_1.value * qc_target_2.value * confidence
				rev2to1 = qc_source_2.value * qc_target_1.value * confidence
		
				if rev2to1 >= min_value or ((n1+n2) < (m * 0.5)):
					if rev2to1 > rev_2to1:
						rev_2to1 = rev2to1
				if rev1to2 >= min_value or ((n1+n2) < (m * 0.5)):
					if rev1to2 > rev_1to2:
						rev_1to2 = rev1to2				
				
			try:
				instance1 = CourseDependency.objects.get(course_source=concept1, course_target=concept2)
				instance1.value = rev_1to2
			except:	
				instance1 = CourseDependency(course_source=concept1, course_target=concept2, value=rev_1to2)	

			try:
				instance2 = CourseDependency.objects.get(course_source=concept2, course_target=concept1)
				instance2.value = rev_2to1
			except:
				instance2 = CourseDependency(course_source=concept2, course_target=concept1, value=rev_2to1)		


			instance1.save()
			instance2.save()
			j = j + 1
		i = i + 1


#This is where it ends

