#!/usr/bin/python

import MySQLdb

#connect to the database
db = MySQLdb.connect("localhost","devanshu","123456","django_db")

#get the cursor
cursor = db.cursor()

sql = "DELETE FROM firstapp_q1q2rightwrong WHERE 1=1;"
cursor.execute(sql)
db.commit()
print "deleting from q1q2rightwrong"

sql = "DELETE FROM firstapp_grade WHERE 1=1;"
cursor.execute(sql)
db.commit()
print "deleting from grade"

sql = "DELETE FROM firstapp_confidencertor WHERE 1=1;"
cursor.execute(sql)
db.commit()
print "deleting from confidencertor"


sql = "DELETE FROM firstapp_confidencewtow WHERE 1=1;"
cursor.execute(sql)
db.commit()
print "deleting from confidencewtow"


sql = "DELETE FROM firstapp_question WHERE 1=1;"
cursor.execute(sql)
db.commit()
print "deleting from question"


sqlList=[]

sql1 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (2,'C programs are converted 
into machine language with the help of ','Editor','Compiler','OS',
'None of the above',2)"""
sqlList.append(sql1)

sql2 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (2,'A character variable can at a time store','1 character','8 characters','256 characters','None of the above',1)"""
sqlList.append(sql2)


sql3 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (2,'The maximum value that an integer constant can have is','-32767','32767','1.7014e+38','depends on the machine',4) """
sqlList.append(sql3)

sql4 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (2,'Which of the following is not a keyword in C ?','for','char','print','case',3) """
sqlList.append(sql4)

sql5 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (3,'What would be the output of the following program:  main( ) 
		{ 
			int a = 300, b = 0, c = 10 ; 
			if ( a >= 400 ) 
			b = 300 ; 
			c = 200 ; 
			printf ( "\n%d %d", b, c ) ; 		
		}','0 10','10 0','0 200','200 300',3) """
sqlList.append(sql5)

sql6 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (3,'What would be the output of the following program:
 main( ) 
			{ 
			int   x = 10, y = 20 ; 
			x == 20 && y != 10 ? printf( "True" ) : printf( "False" ) ; 
			} ','true','flase','compilation error','none of the above',2) """
sqlList.append(sql6)

sql7 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (3,'What would be the output of the following program:
main( ) 
			{  
			int   k, num = 30 ;  
			k = ( num > 5 ? ( num <= 10 ? 100 : 200 ) : 500 ) ;  
			printf ( "\n%d", k ) ;
			} ','500','30','200','100',3) """

sqlList.append(sql7)

sql8 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (3,'What would be the output of the following program:
main( ) 
			{
			int x = 2; 
			if ( x == 2 && x != 0 ) 
				{  
				printf( "\nHello" ) ;  
				} 
			else   
				printf( "Bye" ) ; } ','Hello','Bye','Compilation error','segmentation fault',1) """
sqlList.append(sql8)

sql9 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (4,'How many times does the for loop iterate?
			for ( i = 0; i< 10 ; i = i+2)','5','10','6','11',1) """
sqlList.append(sql9)

sql10 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (4,'In the following code :
			do 
			{
				printf("Hello");
			}
			while ( 4<1);','hello will be printed','hello will not be printed','depends on compiler','depends on interpreter',2) """
sqlList.append(sql10)

sql11 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (4,'Output of following code is
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
','datatype mismatch error','97 11.00','65 1.10','65 1.00',2) """
sqlList.append(sql11)

sql12 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (4,'The value of variable " count" after the outer for loop is :	
			int count = 0;	
			for ( i = 0; i < 5 ; i++)
				for ( j = 0; j<10; j++)
					count++;','5','10','50','100',3) """
sqlList.append(sql12)

sql13 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'What will be the output of following code :
{
		int  num[26], temp ;
		num[0] = 100 ;  
		num[25] = 200 ;
		temp = num[25] ;
		num[25] = num[0] ;
		num[0] = temp ;
		printf ( "\n%d %d", num[0], num[25] ) ; } ','100 200','200 100','100 100','200 200',2) """
sqlList.append(sql13)

sql14 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'What is the starting index of an array?','1','2','3','0',4) """
sqlList.append(sql14)

sql15 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'When an array is passed from main function to other function through call by reference, if the values of array elements in the function change, then the values in main ','change','do not change','change only in the case of call by value','none of the above',1) """
sqlList.append(sql15)

sql16 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql16)

'''
sql17 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql17)

sql18 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql18)

sql19 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql19)

sql20 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql20)

sql21 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql21)

sql22 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql22)

sql23 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql23)

sql24 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql24)

sql25 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql25)

sql26 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql26)

sql27 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql27)

sql28 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql28)

sql29 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql29)

sql30 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql30)

sql31 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql31)

sql32 = """INSERT INTO firstapp_question(COURSE_ID, QUESTION, OPTION1, 
OPTION2, OPTION3, OPTION4, ANSWER) VALUES (5,'The memory locations of consecutive elements in array are :','consecutive','differ by 2','differ by 6','differ by 8',1) """
sqlList.append(sql32)
'''

i = 1
for sql in sqlList:
	try:
		#execute a sql query
		cursor.execute(sql)
	        print "here, OK!"	
		print "Added the question " + str(i) + "into database"
		i = i + 1
		#commit changes
		db.commit()
	except Exception as inst:
		
		# rollback in case there is any error
		db.rollback()
		print "Couldn't add question no. " + str(i) + "!!"
		print type(inst)


sql = "DELETE FROM firstapp_q1q2rightwrong WHERE 1=1;"
cursor.execute(sql)
db.commit()

sql = "SELECT * FROM firstapp_student;"
cursor.execute(sql)
wrong = len(cursor.fetchall())

sql = "SELECT * FROM firstapp_question;"
cursor.execute(sql)

results = cursor.fetchall()

i = 0
length = len(results)
print length
while i < length:
	print "i = " + str(i) + " results[i][0] " + str(results[i][0])
	j = i + 1
	while j < length:
		print "j = " + str(j) + " results[j][0] " + str(results[j][0])
		sql = """INSERT INTO firstapp_q1q2rightwrong(`question_x_id`, `question_y_id`, `right`,`wrong`) VALUES ('%s','%s','%d','%d');""" % (results[i][0],results[j][0],0,wrong)
		cursor.execute(sql)
		db.commit()
		j = j + 1
	i = i + 1

i = 0
while i < length:
	sql = """INSERT INTO firstapp_q1q2rightwrong(`question_x_id`, `question_y_id`, `right`,`wrong`) VALUES ('%s','%s','%d','%d');""" % (results[i][0],results[i][0],0,wrong)
	cursor.execute(sql)
	db.commit()
	i = i + 1

sql = "SELECT * FROM firstapp_q1q2rightwrong;"
cursor.execute(sql)
List = cursor.fetchall()
print "items added : " + str(len(List))

cursor.close()
db.close()
