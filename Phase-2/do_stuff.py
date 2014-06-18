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

cursor.close()
db.close()
