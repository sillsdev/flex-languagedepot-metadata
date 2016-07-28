from capabilities.capability import capability
import subprocess # used for bash commands (when required), unix-only
from pipes import quote # used to sanitize bash input when complex commands are required, unix-only

class tasks(capability):

    def analyze(projectPath):
        names = subprocess.check_output('cd %s && hg log --template "{author}\n" | sort | uniq' \
        % quote(projectPath), shell=True).decode('utf-8').replace('\n', ', ')
        number = subprocess.check_output('cd %s && hg log --template "{author}\n" | sort | uniq | wc -l' \
        % quote(projectPath), shell=True).decode('utf-8')
        return [names[:-2], number]

    def updateDb(dbConn, py_name, value):
        # print(py_name +" "+ value)
        cur = dbConn.cursor() # cursor to make changes
        cur.execute( """UPDATE project.metadata
            SET
            committerNames = %s,
            committerNumber = %s
            WHERE name = %s;""", (value[0], value[1], py_name) )
        dbConn.commit() # save changes to db

    def getColumns():
        return [
        ['committerNames', 'text'],
        ['committerNumber', 'int']
        ]
