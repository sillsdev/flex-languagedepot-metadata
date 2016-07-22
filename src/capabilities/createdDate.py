from capabilities.capability import capability
import subprocess # used for bash commands (when required), unix-only
from pipes import quote # used to sanitize bash input when complex commands are required, unix-only

class tasks(capability):

    # goes to the folder, gets the first commit, and filters out the date
    # sometimes the project doesn't have a first commit, so it returns the zeroth commit
    def analyze(projectPath):
        try:
            catch = subprocess.check_output( 'cd %s && hg log -r 1 --template "{date|shortdate}"' \
            % quote(projectPath), shell=True)
        except(subprocess.CalledProcessError):
            return subprocess.check_output( 'cd %s && hg log -r 0 --template "{date|shortdate}"' \
            % quote(projectPath), shell=True).decode('utf-8')
        else:
            return catch.decode('utf-8')

    def updateDb(dbConn, py_name, value):
        # print(py_name +" "+ value)
        cur = dbConn.cursor() # cursor to make changes
        cur.execute( "UPDATE project.metadata SET createdDate = %s WHERE name = %s;", (value, py_name) )
        dbConn.commit() # save changes to db

    def getColumns():
        return ['createdDate','date']

    # end of tasks
