from capabilities.capability import capability
import subprocess # used for bash commands (when required), unix-only
from pipes import quote # used to sanitize bash input when complex commands are required, unix-only
import psycopg2

class tasks(capability):

    def analyze(projectPath):
        return subprocess.check_output('cd %s && hg log --template "{author}\n" | sort | uniq' \
        % quote(projectPath), shell=True).decode('utf-8').split('\n')

    def updateDb(dbConn, py_name, value):
        # print(py_name +" "+ value)
        conn = psycopg2.connect(dbConn) # connection to the db
        cur = conn.cursor() # cursor to make changes
        cur.execute( "UPDATE project.metadata SET committerNames = %s WHERE name = %s;", (value, py_name) )
        conn.commit() # save changes to db

    def getColumns():
        return 'committerNames'
