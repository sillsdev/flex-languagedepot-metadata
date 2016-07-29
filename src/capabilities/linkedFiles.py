from capabilities.capability import capability
import glob

class tasks(capability):

    def analyze(projectPath):
        # pictures
        if glob.glob('%s/LinkedFiles/Pictures/*' % projectPath):
            fileList = glob.glob('%s/LinkedFiles/Pictures/*' % projectPath)
            pictures = len(fileList)
        else:
            pictures = 0

        # audiovisual
        if glob.glob('%s/LinkedFiles/AudioVisual/*' % projectPath):
            fileList = glob.glob('%s/LinkedFiles/AudioVisual/*' % projectPath)
            audiovisual = len(fileList)
        else:
            audiovisual = 0

        return [
        pictures,
        audiovisual
        ]

    def updateDb(dbConn, py_name, value):
        cur = dbConn.cursor() # cursor to make changes
        cur.execute( """UPDATE project.metadata SET
        pictures = %s,
        audiovisual = %s
        WHERE name = %s;""", (value[0], value[1], py_name) )
        dbConn.commit() # save changes to db

    def getColumns():
        return [
        ['pictures', 'int'],
        ['audiovisual', 'int']
        ]
