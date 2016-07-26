from capabilities.capability import capability
import glob
import xml.etree.ElementTree as ET

class tasks(capability):

    # searches every xml file in the lexicon for <Text> tags
    # finds each file in the folder, parses it, and looks for the tag however many times
    def analyze(projectPath):
        texts = 0
        listOfLexicons = glob.glob( projectPath + 'Linguistics/Lexicon/Lexicon_0*.lexdb' )
        for lex in listOfLexicons:
            # open
            tree = ET.parse(lex)
            root = tree.getroot()
            # scan
            for text in root.iter('Text'):
                texts+=1

        return texts


    def updateDb(dbConn, py_name, value):
        # print(py_name +" "+ value)
        cur = dbConn.cursor() # cursor to make changes
        cur.execute( "UPDATE project.metadata SET classCount_text = %s WHERE name = %s;", (value, py_name) )
        dbConn.commit() # save changes to db

    def getColumns():
        return ['classCount_text', 'int']
