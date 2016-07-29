from capabilities.capability import capability
import os
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
                    try:
                        vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[2]
                    except(IndexError):
                        pass
                    else:
                        analysis[ vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[2] ] = None
                        try:
                            vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[3]
                        except(IndexError):
                            pass
                        else:
                            analysis[ vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[3] ] = None
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
                    try:
                        vroot.find('.//CurVernWss/Uni').text.split(' ')[2]
                    except(IndexError):
                        pass
                    else:
                        vernacular[ vroot.find('.//CurVernWss/Uni').text.split(' ')[2] ] = None
                        try:
                            vroot.find('.//CurVernWss/Uni').text.split(' ')[3]
                        except(IndexError):
                            pass
                        else:
                            vernacular[ vroot.find('.//CurVernWss/Uni').text.split(' ')[3] ] = None

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
                        # add a letter to the writing system if it's not there already
                        if tag.text: tempList = {x for x in tag.text.strip()}
                        if analysis[ws] != None:
                            analysis[ws].update(tempList)
                        else:
                            analysis[ws] = tempList
                    if ws in vernacular:
                        # add a letter to the writing system if it's not there already
                        if tag.text: tempList = {x for x in tag.text.strip()}
                        if vernacular[ws] != None:
                            vernacular[ws].update(tempList)
                        else:
                            vernacular[ws] = tempList

                for tag in root.iter('Uni'):
                    ws = tag.get('ws')
                    # check if the writing system is in the inventory or not
                    if ws in analysis:
                        # add a letter to the writing system if it's not there already
                        if tag.text: tempList = {x for x in tag.text.strip()}
                        if analysis[ws] != None:
                            analysis[ws].update(tempList)
                        else:
                            analysis[ws] = tempList
                    if ws in vernacular:
                        # add a letter to the writing system if it's not there already
                        if tag.text: tempList = {x for x in tag.text.strip()}
                        if vernacular[ws] != None:
                            vernacular[ws].update(tempList)
                        else:
                            vernacular[ws] = tempList

                for tag in root.iter('AUni'):
                    ws = tag.get('ws')
                    # check if the writing system is in the inventory or not
                    if ws in analysis:
                        # add a letter to the writing system if it's not there already
                        if tag.text: tempList = {x for x in tag.text.strip()}
                        if analysis[ws] != None:
                            analysis[ws].update(tempList)
                        else:
                            analysis[ws] = tempList
                    if ws in vernacular:
                        # add a letter to the writing system if it's not there already
                        if tag.text: tempList = {x for x in tag.text.strip()}
                        if vernacular[ws] != None:
                            vernacular[ws].update(tempList)
                        else:
                            vernacular[ws] = tempList

                # end of writing system check

            # end of lexicon check

        # stem and root configuration
        customStemCount = 0
        customRootCount = 0
        customStemCopy = 0
        customRootCopy = 0
        if glob.glob('%s/ConfigurationSettings/*' % projectPath):
            dirfiles = glob.glob('%s/ConfigurationSettings/*' % projectPath)
            listOfLayouts = [ f for f in dirfiles if not os.path.isdir(f)]
            for fwlayout in listOfLayouts:
                tree = ET.parse(fwlayout)
                root = tree.getroot()

                for tag in root.iter('layout'):
                    typeTag = tag.get('type')
                    name = tag.get('name')

                    # stem count and copy count
                    if typeTag == 'jtview' and 'publishStem' in name:
                        if name.replace('publishStem#', '') == int:
                            customStemCopy += 1
                        else:
                            customRootCount += 1

                    # root count and copy count
                    if typeTag == 'jtview' and 'publishRoot' in name:
                        if name.replace('publishRoot#', '') == int:
                            customRootCopy += 1
                        else:
                            customRootCount += 1

            # end of stem and root / layout config


        dataList = [
        texts,
        None, # key for first analysis alphabet
        None, # value for first analysis alphabet
        None, # key for second analysis alphabet
        None, # value for second analysis alphabet
        None, # key for third analysis alphabet
        None, # value for third analysis alphabet
        None, # key for fourth analysis alphabet
        None, # value for fourth analysis alphabet
        None, # key for first vernacular alphabet
        None, # value for first vernacular alphabet
        None, # key for second vernacular alphabet
        None, # value for second vernacular alphabet
        None, # key for third vernacular alphabet
        None, # value for third vernacular alphabet
        None, # key for fourth vernacular alphabet
        None, # value for fourth vernacular alphabet
        customStemCount,
        customRootCount,
        customStemCopy,
        customRootCopy
        ]

        try:
            list(analysis.keys())[0]
            ''.join( list(analysis.values())[0] )
        except(IndexError):
            pass
        except(TypeError):
            pass
        else:
            dataList[1] = list(analysis.keys())[0]
            dataList[2] = ''.join( sorted( list(analysis.values())[0] ) )
            try:
                list(analysis.keys())[1]
                ''.join( list(analysis.values())[1] )
            except(IndexError):
                pass
            except(TypeError):
                pass
            else:
                dataList[3] = list(analysis.keys())[1]
                dataList[4] = ''.join( sorted( list(analysis.values())[1] ) )
                try:
                    list(analysis.keys())[2]
                    ''.join( list(analysis.values())[2] )
                except(IndexError):
                    pass
                except(TypeError):
                    pass
                else:
                    dataList[5] = list(analysis.keys())[2]
                    dataList[6] = ''.join( sorted( list(analysis.values())[2] ) )
                    try:
                        list(analysis.keys())[3]
                        ''.join( list(analysis.values())[3] )
                    except(IndexError):
                        pass
                    except(TypeError):
                        pass
                    else:
                        dataList[7] = list(analysis.keys())[3]
                        dataList[8] = ''.join( sorted( list(analysis.values())[3] ) )
        try:
            list(vernacular.keys())[0]
            ''.join( list(vernacular.values())[0] )
        except(IndexError):
            pass
        except(TypeError):
            pass
        else:
            dataList[9] = list(vernacular.keys())[0]
            dataList[10] = ''.join( sorted( list(vernacular.values())[0] ) )
            try:
                list(vernacular.keys())[1]
                ''.join( list(vernacular.values())[1] )
            except(IndexError):
                pass
            except(TypeError):
                pass
            else:
                dataList[11] = list(vernacular.keys())[1]
                dataList[12] = ''.join( sorted( list(vernacular.values())[1] ) )
                try:
                    list(vernacular.keys())[2]
                    ''.join( list(vernacular.values())[2] )
                except(IndexError):
                    pass
                except(TypeError):
                    pass
                else:
                    dataList[13] = list(vernacular.keys())[2]
                    dataList[14] = ''.join( sorted( list(vernacular.values())[2] ) )
                    try:
                        list(vernacular.keys())[3]
                        ''.join( list(vernacular.values())[3] )
                    except(IndexError):
                        pass
                    except(TypeError):
                        pass
                    else:
                        dataList[15] = list(vernacular.keys())[3]
                        dataList[16] = ''.join( sorted( list(vernacular.values())[3] ) )

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
        analysis3_code = %s,
        analysis3_characterInventory = %s,
        analysis4_code = %s,
        analysis4_characterInventory = %s,
        vernacular1_code = %s,
        vernacular1_characterInventory = %s,
        vernacular2_code = %s,
        vernacular2_characterInventory = %s,
        vernacular3_code = %s,
        vernacular3_characterInventory = %s,
        vernacular4_code = %s,
        vernacular4_characterInventory = %s,
        customStemConfigurationCount = %s,
        customRootConfigurationCount = %s,
        stemConfigurationCopyCount = %s,
        rootConfigurationCopyCount = %s
        WHERE name = %s;""",
        (value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8],
        value[9], value[10], value[11], value[12], value[13], value[14], value[15], value[16],
        value[17], value[18], value[19], value[20],
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
        ['analysis3_code', 'varchar(80)'],
        ['analysis3_characterInventory', 'text'],
        ['analysis4_code', 'varchar(80)'],
        ['analysis4_characterInventory', 'text'],
        ['vernacular1_code', 'varchar(80)'],
        ['vernacular1_characterInventory', 'text'],
        ['vernacular2_code', 'varchar(80)'],
        ['vernacular2_characterInventory', 'text'],
        ['vernacular3_code', 'varchar(80)'],
        ['vernacular3_characterInventory', 'text'],
        ['vernacular4_code', 'varchar(80)'],
        ['vernacular4_characterInventory', 'text'],
        ['customStemConfigurationCount', 'int'],
        ['customRootConfigurationCount', 'int'],
        ['stemConfigurationCopyCount', 'int'],
        ['rootConfigurationCopyCount', 'int']
        ]
