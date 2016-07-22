from capabilities.capability import capability
import subprocess # used for bash commands (when required), unix-only
from pipes import quote # used to sanitize bash input when complex commands are required, unix-only

class tasks(capability):

    # goes to the folder, gets the tip, and filters out the date
    def analyze(projectPath):
        return subprocess.check_output( 'cd %s && hg tip --template "{date|shortdate}"' \
        % quote(projectPath), shell=True).decode('utf-8')

    def updateDb(dbConn, py_name, value):
        # print(py_name +" "+ value)
        cur = dbConn.cursor() # cursor to make changes
        cur.execute( "UPDATE project.metadata SET modifiedDate = %s WHERE name = %s;", (value, py_name) )
        dbConn.commit() # save changes to db

    def getColumns():
        return ['modifiedDate','date']

    # end of tasks
