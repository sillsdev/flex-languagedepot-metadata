from capabilities.capability import capability
import subprocess # used for bash commands (when required), unix-only. safer than os.system()
from pipes import quote # used to sanitize bash input when complex commands are required, unix-only

class tasks(capability):

    # goes to the folder, gets the tip of the mercurial project, and filters out its commit number
    def analyze(projectPath):
        return int( subprocess.check_output( 'cd %s && hg tip --template "{rev}"' \
        % quote(projectPath), shell=True ).decode('utf-8') )

    def updateDb(dbConn, py_name, value):
        # print(py_name +" "+ value)
        cur = dbConn.cursor() # cursor to make changes
        cur.execute( "UPDATE project.metadata SET numberOfRevisions = %s WHERE name = %s;", (value, py_name) )
        dbConn.commit() # save changes to db

    def getColumns():
        return ['numberOfRevisions','int']

    # end of tasks
