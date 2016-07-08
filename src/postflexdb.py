#!/usr/bin/python
import psycopg2

def connect():
    # Connection string, replace placeholder with better password
    conn_string = "host=localhost dbname=languagedepot-metadata user=postgres password=placeholder"

    # prove that we are connecting to the database:
    print ("Connecting to database\n ->%s") % (conn_string)
    conn = psycopg2.connect(conn_string)
    print ("Connected!\n")

    # make a cursor object which can be used to perform queries
    global cur
    cur = conn.cursor()

    # end of connect()

def addItems(py_name, py_id, py_projectCode, py_projectSizeInMB, py_numberOfRevisions, py_createdDate, py_modifiedDate):
    # seven items
    assert type(py_name) is StringType, "py_name is not a string"
    assert type(py_id) is IntType, "py_id is not an integer"
    assert type(py_projectCode) is StringType, "py_name is not a string"
    assert type(py_projectSizeInMB) is IntType, "py_projectCode is not an integer"
    assert type(py_numberOfRevisions) is IntType, "py_numberOfRevisions is not an integer"
    assert type(py_createdDate) is datetime.date, "py_createdDate is not a date"
    assert type(py_modifiedDate) is datetime.date, "py_modifiedDate is not a date"
    # insert the new items
    cur.execute("INSERT INTO project.metadata VALUES (%s, %s, %s, %s, %s, %s, %s);",
        (py_name, py_id, py_projectCode, py_projectSizeInMB, py_numberOfRevisions, py_createdDate, py_modifiedDate) )

    # query and print the result, this can be commented out later
    cur.execute("SELECT * FROM project.metadata WHERE name = %s;", (py_name,))
    query = cur.fetchone()
    print(query)

    # end of addItems()

def commit():
    # the previous commands are all suggestions that sit in the runtime.
    # all changes wouldn't actually affect the actual database until this line:
    conn.commit()

    # end of commit()

if __name__ == '__main__':
    import sys
    connect()
    addItems(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7],)
    #commit()
