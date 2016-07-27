from capabilities.capability import capability
import glob
import xml.etree.ElementTree as ET


class tasks(capability):

    # searches every xml file in the lexicon for <Text> tags
    # finds each file in the folder, parses it, and looks for the tag however many times
    def analyze(projectPath):
        # vernacular writing systems
        alphabet = {}
        if glob.glob('%s/General/LanguageProject.langproj' % projectPath):
            vtree = ET.parse('%s/General/LanguageProject.langproj' % projectPath)
            vroot = vtree.getroot()

            alphabet[ vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[0] ] = []
            try:
                vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[1]
            except(IndexError):
                pass
            else:
                alphabet[ vroot.find('.//CurAnalysisWss/Uni').text.split(' ')[1] ] = []

            alphabet[ vroot.find('.//CurVernWss/Uni').text.split(' ')[0] ] = []
            try:
                vroot.find('.//CurVernWss/Uni').text.split(' ')[1]
            except(IndexError):
                pass
            else:
                alphabet[ vroot.find('.//CurVernWss/Uni').text.split(' ')[1] ] = []

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
                    if ws in alphabet:
                        # won't return None automatically
                        if tag.text:
                            for letter in tag.text.strip():
                                # check if all the letters are in the writing system's list
                                if letter not in alphabet[ws]:
                                    alphabet[ws].append(letter)

                for tag in root.iter('Uni'):
                    ws = tag.get('ws')
                    # check if the writing system is in the inventory or not
                    if ws in alphabet:
                        # won't return None automatically
                        if tag.text:
                            for letter in tag.text.strip():
                                # check if all the letters are in the writing system's list
                                if letter not in alphabet[ws]:
                                    alphabet[ws].append(letter)

                for tag in root.iter('AUni'):
                    ws = tag.get('ws')
                    # check if the writing system is in the inventory or not
                    if ws in alphabet:
                        # won't return None automatically
                        if tag.text:
                            for letter in tag.text.strip():
                                # check if all the letters are in the writing system's list
                                if letter not in alphabet[ws]:
                                    alphabet[ws].append(letter)

                # end of writing system check

            # end of lexicon check

        try:
            list(alphabet.keys())[0]
        except(IndexError):
            return [
            texts,
            # lexentries,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None
            ]
        else:
            try:
                list(alphabet.keys())[1]
            except(IndexError):
                return [
                texts,
                # lexentries,
                list(alphabet.keys())[0],
                list(alphabet.values())[0],
                None,
                None,
                None,
                None,
                None,
                None
                ]
            else:
                try:
                    list(alphabet.keys())[2]
                except(IndexError):
                    return [
                    texts,
                    # lexentries,
                    list(alphabet.keys())[0],
                    list(alphabet.values())[0],
                    list(alphabet.keys())[1],
                    list(alphabet.values())[1],
                    None,
                    None,
                    None,
                    None,
                    ]
                else:
                    try:
                        list(alphabet.keys())[3]
                    except(IndexError):
                        return [
                        texts,
                        # lexentries,
                        list(alphabet.keys())[0],
                        list(alphabet.values())[0],
                        list(alphabet.keys())[1],
                        list(alphabet.values())[1],
                        list(alphabet.keys())[2],
                        list(alphabet.values())[2],
                        None,
                        None,
                        ]
                    else:
                        return [
                        texts,
                        # lexentries,
                        list(alphabet.keys())[0],
                        list(alphabet.values())[0],
                        list(alphabet.keys())[1],
                        list(alphabet.values())[1],
                        list(alphabet.keys())[2],
                        list(alphabet.values())[2],
                        list(alphabet.keys())[3],
                        list(alphabet.values())[3],
                        ]

    def updateDb(dbConn, py_name, value):
        # lexEntry = %s,
        cur = dbConn.cursor() # cursor to make changes
        cur.execute( """UPDATE project.metadata SET
        classCount_text = %s,
        vernacular1_code = %s,
        vernacular1_characterInventory = %s,
        vernacular2_code = %s,
        vernacular2_characterInventory = %s
        WHERE name = %s;""", (value[0], value[1], value[2], value[3], value[4], py_name) )
        dbConn.commit() # save changes to db

    def getColumns():
        return [
        ['classCount_text', 'int'],
        # ['lexEntry', 'int'],
        ['vernacular1_code', 'varchar(80)'],
        ['vernacular1_characterInventory', 'text[]'],
        ['vernacular2_code', 'varchar(80)'],
        ['vernacular2_characterInventory', 'text[]']
        ]
