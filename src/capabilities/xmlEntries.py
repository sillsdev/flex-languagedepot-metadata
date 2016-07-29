from capabilities.capability import capability
import glob
import xml.etree.ElementTree as ET


class tasks(capability):

    # searches every xml file in the lexicon for <Text> tags
    # finds each file in the folder, parses it, and looks for the tag however many times
    def analyze(projectPath):
        # analysis & vernacular writing systems
        analysis = {}
        vernacular = {}
        if glob.glob('%s/General/LanguageProject.langproj' % projectPath):
            vtree = ET.parse('%s/General/LanguageProject.langproj' % projectPath)
            vroot = vtree.getroot()
            # analysis
            try:
                vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[0]
            except(IndexError):
                pass
            else:
                analysis[ vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[0] ] = None
                try:
                    vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[1]
                except(IndexError):
                    pass
                else:
                    analysis[ vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[1] ] = None
            # vernacular
            try:
                vroot.find('.//CurVernWss/Uni').text.split(' ')[0]
            except(IndexError):
                pass
            else:
                vernacular[ vroot.find('.//CurVernWss/Uni').text.split(' ')[0] ] = None
                try:
                    vroot.find('.//CurVernWss/Uni').text.split(' ')[1]
                except(IndexError):
                    pass
                else:
                    vernacular[ vroot.find('.//CurVernWss/Uni').text.split(' ')[1] ] = None

            # end of analysis & vernacular check

        # Lexicon
        texts = 0
        lexentries = 0
        if glob.glob('%s/Linguistics/Lexicon/Lexicon_**.lexdb' % projectPath):
            listOfLexicons = glob.glob('%s/Linguistics/Lexicon/Lexicon_**.lexdb' % projectPath)
            for lex in listOfLexicons:
                # open
                tree = ET.parse(lex)
                root = tree.getroot()
                # scan
                for tag in root.iter('Text'): texts+=1

                # for tag in root.iter('LexEntry'): lexentries+=1

                for tag in root.iter('Str'):
                    ws = tag.get('ws')
                    # check if the writing system is in the inventory or not
                    if ws in analysis:
                        if tag.text:
                            # add a letter to the writing system if it's not there already
                            tempList = []
                            tempList = {x for x in tag.text.strip()}
                            analysis[ws] = ''.join( sorted(tempList) )
                    if ws in vernacular:
                        if tag.text:
                            # add a letter to the writing system if it's not there already
                            tempList = []
                            tempList = {x for x in tag.text.strip()}
                            analysis[ws] = ''.join( sorted(tempList) )

                for tag in root.iter('Uni'):
                    ws = tag.get('ws')
                    # check if the writing system is in the inventory or not
                    if ws in analysis:
                        if tag.text:
                            # add a letter to the writing system if it's not there already
                            tempList = []
                            tempList = {x for x in tag.text.strip()}
                            analysis[ws] = ''.join( sorted(tempList) )
                    if ws in vernacular:
                        if tag.text:
                            # add a letter to the writing system if it's not there already
                            tempList = []
                            tempList = {x for x in tag.text.strip()}
                            analysis[ws] = ''.join( sorted(tempList) )

                for tag in root.iter('AUni'):
                    ws = tag.get('ws')
                    # check if the writing system is in the inventory or not
                    if ws in analysis:
                        # won't return None automatically
                        if tag.text:
                            # add a letter to the writing system if it's not there already
                            tempList = []
                            tempList = {x for x in tag.text.strip()}
                            analysis[ws] = ''.join( sorted(tempList) )
                    if ws in vernacular:
                        # won't return None automatically
                        if tag.text:
                            # add a letter to the writing system if it's not there already
                            tempList = []
                            tempList = {x for x in tag.text.strip()}
                            analysis[ws] = ''.join( sorted(tempList) )

                # end of writing system check

            # end of lexicon check

        dataList = [
        texts,
        None, # key for first analysis alphabet
        None, # value for first analysis alphabet
        None, # key for second analysis alphabet
        None, # value for second analysis alphabet
        None, # key for first vernacular alphabet
        None, # value for first vernacular alphabet
        None, # key for second vernacular alphabet
        None, # value for second vernacular alphabet
        ]

        try:
            list(analysis.keys())[0]
        except(IndexError):
            pass
        else:
            dataList[1] = list(analysis.keys())[0]
            dataList[2] = list(analysis.values())[0]
            try:
                list(analysis.keys())[1]
            except(IndexError):
                pass
            else:
                dataList[3] = list(analysis.keys())[1]
                dataList[4] = list(analysis.values())[1]
        try:
            list(vernacular.keys())[0]
        except(IndexError):
            pass
        else:
            dataList[5] = list(vernacular.keys())[0]
            dataList[6] = list(vernacular.values())[0]
            try:
                list(vernacular.keys())[1]
            except(IndexError):
                pass
            else:
                dataList[7] = list(vernacular.keys())[1]
                dataList[8] = list(vernacular.values())[1]

        # end of EAFP

        return dataList


    def updateDb(dbConn, py_name, value):
        # lexEntry = %s,
        cur = dbConn.cursor() # cursor to make changes
        cur.execute( """UPDATE project.metadata SET
        classCount_text = %s,
        analysis1_code = %s,
        analysis1_characterInventory = %s,
        analysis2_code = %s,
        analysis2_characterInventory = %s,
        vernacular1_code = %s,
        vernacular1_characterInventory = %s,
        vernacular2_code = %s,
        vernacular2_characterInventory = %s
        WHERE name = %s;""",
        (value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8],
        py_name) )
        dbConn.commit() # save changes to db

    def getColumns():
        return [
        ['classCount_text', 'int'],
        # ['lexEntry', 'int'],
        ['analysis1_code', 'varchar(80)'],
        ['analysis1_characterInventory', 'text'],
        ['analysis2_code', 'varchar(80)'],
        ['analysis2_characterInventory', 'text'],
        ['vernacular1_code', 'varchar(80)'],
        ['vernacular1_characterInventory', 'text'],
        ['vernacular2_code', 'varchar(80)'],
        ['vernacular2_characterInventory', 'text']
        ]
