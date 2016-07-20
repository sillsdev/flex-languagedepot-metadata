from abc import ABCMeta, abstractmethod

class capability(metaclass=ABCMeta):

    # used during initialization. returns a string for the single catergory
    # of information the capability will extract, or a list of strings for
    # each category the capability will extract.
    @abstractmethod
    def getColumns(x):
        raise NotImplementedError()

    # analyzes the database for specific information
    @abstractmethod
    def analyze(projectFolderPath):
        raise NotImplementedError()

    # updates the database once the info is extracted
    @abstractmethod
    def updateDb(dbConnection, py_name, value):
        raise NotImplementedError()

#
#
#
#
#
#
#
