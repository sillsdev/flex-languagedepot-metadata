from capabilities.capability import capability
import subprocess # used for bash commands (when required), unix-only
from pipes import quote # used to sanitize bash input when complex commands are required, unix-only

class tasks(capability):

    # the standard command for getting folder size is filtered down to the mere number
    def analyze(projectPath):
        catch = subprocess.check_output( 'du -hcs %s | sed "2q;d"' % \
        quote(projectPath), shell=True ).decode('utf-8').strip('M\ttotal\n')
        if ('K' in catch):
            return 1
        else:
            return int(round(float(catch)))

    def updateDb(dbConn, py_name, value):
        # print(py_name +" "+ value)
        cur = dbConn.cursor() # cursor to make changes
        cur.execute( "UPDATE project.metadata SET projectSizeInMB = %s WHERE name = %s;", (value, py_name) )
        dbConn.commit() # save changes to db

    def getColumns():
        return ['projectSizeInMB','int']

    # end of tasks
