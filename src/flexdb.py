#!/usr/bin/python
import sys
import psycopg2
from types import *

def connect(passwd):
    # Connection string
    conn_string = "host=localhost dbname=languagedepot-metadata user=postgres password=" + passwd

    # prove that we are connecting to the database:
    print ("Connecting to database\n ->%s") % (conn_string)
    
    global conn # needs to be global in order to commit changes
    conn = psycopg2.connect(conn_string)
    print ("Connected!\n")

    global cur # a cursor object which can be used to perform SQL actions
    cur = conn.cursor()

    # end of connect()

def addItems(py_name, py_projectCode, py_projectSizeInMB, py_numberOfRevisions, py_createdDate, py_modifiedDate):
    # six items
    assert type(py_name) is StringType, "py_name is not a string"
    assert type(py_projectCode) is StringType, "py_projectCode is not a string"
    assert type(py_projectSizeInMB) is IntType, "py_projectSizeInMB is not an integer"
    assert type(py_numberOfRevisions) is IntType, "py_numberOfRevisions is not an integer"
    assert ( len(py_createdDate) == 10 and py_createdDate[:4].isdigit() and py_createdDate[5:7].isdigit() \
    and '-' in py_createdDate[4:5] and '-' in py_createdDate[7:8] ) \
     is True, "py_createdDate is not in the correct format. The correct format is '2016-12-16', your date is %s." % (py_createdDate)
    assert ( len(py_modifiedDate) == 10 and py_modifiedDate[:4].isdigit() and py_modifiedDate[5:7].isdigit() \
    and '-' in py_modifiedDate[4:5] and '-' in py_modifiedDate[7:8] ) \
     is True, "py_modifiedDate is not in the correct format. The correct format is '2016-12-16', your date is %s." % (py_modifiedDate)

    # insert the new items
    cur.execute("""INSERT INTO project.metadata (name, projectCode, projectSizeInMB, numberOfRevisions, createdDate, modifiedDate)
     VALUES (%s, %s, %s, %s, %s, %s);""",
        (py_name, py_projectCode, py_projectSizeInMB, py_numberOfRevisions, py_createdDate, py_modifiedDate) )

    # query and print the result, this can be commented out later
    #cur.execute("SELECT * FROM project.metadata WHERE name = %s;", (py_name,))
    #query = cur.fetchone()
    #print(query)

    # end of addItems()

def commit():
    # the previous commands are all suggestions that sit in the runtime.
    # all changes wouldn't actually affect the actual database until this line:
    conn.commit()

    # end of commit()

if __name__ == '__main__':
    usr = raw_input("Password:\n")
    connect(usr)
    entered_name = raw_input("Name:\n")
    entered_size = input("Size:\n")
    entered_revs = input("Revisions:\n")
    entered_1stc = raw_input("Date of first commit:\n")
    entered_lstc = raw_input("Date of last commit:\n")
    addItems(entered_name, entered_name, entered_size, entered_revs, entered_1stc, entered_lstc)
    #commit()
