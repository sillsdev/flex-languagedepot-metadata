from capabilities.capability import capability
import subprocess # used for bash commands (when required), unix-only
from pipes import quote # used to sanitize bash input when complex commands are required, unix-only

class tasks(capability):

    # the standard command for getting folder size is filtered down to the mere number
    def analyze(projectPath):
        # total size
        total1 = subprocess.check_output( 'du -mcs %s | sed "2q;d"' % \
        quote(projectPath), shell=True ).decode('utf-8').strip('\ttotal\n')
        total = int(round(float(total1)))

        # project size
        project1 = subprocess.check_output( 'du --exclude=.hg -mcs %s | sed "2q;d"' % \
        quote(projectPath), shell=True ).decode('utf-8').strip('\ttotal\n')
        project = int(round(float(project1)))

        # mercurial repo size
        hgsize1 = subprocess.check_output( 'du -mcs %s/.hg | sed "2q;d"' % \
        quote(projectPath), shell=True ).decode('utf-8').strip('\ttotal\n')
        hgsize = int(round(float(hgsize1)))

        return [total, project, hgsize]

    def updateDb(dbConn, py_name, value):
        # print(py_name +" "+ value)
        cur = dbConn.cursor() # cursor to make changes
        cur.execute( """UPDATE project.metadata SET
        totalSizeInMB = %s,
        projectSizeInMB = %s,
        repoSizeInMB = %s
        WHERE name = %s;""", (value[0], value[1], value[2], py_name) )
        dbConn.commit() # save changes to db

    def getColumns():
        return [
        ['totalSizeInMB','int'],
        ['projectSizeInMB', 'int'],
        ['repoSizeInMB', 'int']
        ]

    # end of tasks
