from abc import ABCMeta, abstractmethod

class capability(metaclass=ABCMeta):

    @abstractmethod
    def analyze(projectFolderPath):
        raise NotImplementedError()

    @abstractmethod
    def updateDb(dbConnection, value):
        raise NotImplementedError()
