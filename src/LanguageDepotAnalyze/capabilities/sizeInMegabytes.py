import capability

class sizeInMegabytes(capability):

    def analyze(projectPath):
        return 5

    def updateDb(dbConnection, value):
        # use an UPDATE statement, not an INSERT statement
        return true
