from capabilities.capability import capability

# Used for bash commands (when required), unix-only
import subprocess

# used to sanitize bash input when complex commands are required, unix-only
from pipes import quote
import glob

from enum import Enum
from collections import OrderedDict


class tasks(capability):

    # Class
    xml = Enum('SearchTypes', 'tag class_')

    # Define what to search for, in which directories, and whether it is a
    # class or an XML tag being searched for.
    searchItems = OrderedDict([
        ('Linguistics/Lexicon', [
                ('LexEntry', xml.tag),
                ('LexSense', xml.class_),
                ('LexPronunciation', xml.class_),
                ('LexExampleSentence', xml.class_),
                ('LexReference', xml.tag),
                ('LexEntryRef', xml.class_),
                ('CmPicture', xml.class_)
            ]
         ),
        ('Linguistics/Reversals', [
                ('ReversalIndex', xml.tag),
                ('ReversalIndexEntry', xml.tag)
            ]
         ),
        ('Other/Books', [
                ('ScrBook', xml.tag),
                ('ScrSection', xml.class_),
                ('ScrTextPara', xml.class_)
            ]
         ),
        ('Linguistics/Inventory', [
                ('WfiWordform', xml.tag),
                ('WfiAnalysis', xml.tag),
                ('WfiGloss', xml.tag),
                ('WfiMorphBundle', xml.class_)
            ],
         ),
        ('Linguistics/TextCorpus', [
                ('StTxtPara', xml.class_),
                ('TextTag', xml.tag)
            ],
         ),
        ('Anthropology', [
                ('RnGenericRec', xml.tag)
            ],
         ),
        ('General', [
                ('CmFile', xml.tag)
            ],
         ),
        ('Linguistics/Discourse', [
                ('ConstChartRow', xml.class_),
                ('ConstChartTag', xml.class_),
                ('DsChart', xml.tag)
            ]
         )
    ])

    # various xml tags are grabbed with the grep command:
    def analyze(projectPath):

        results = []
        quote(projectPath)

        for directory, searchItem in tasks.searchItems.items():
            # Only search a directory if it exists
            if not glob.glob(projectPath + '/' + directory + '/*'):
                # Append None for each search term that we can't search for
                results.extend([None] * len(searchItem))
                # Go to next search dir
                continue

            for tagOrClass in searchItem:
                if tagOrClass[1] == tasks.xml.class_:
                    searchFor = 'class=\"{}\"'.format(tagOrClass[0])
                else:
                    assert tagOrClass[1] == tasks.xml.tag
                    searchFor = '</{}>'.format(tagOrClass[0])

                current_dir = '{}/{}/*'.format(projectPath, directory)
                args = "grep -r '{}' {} | wc -l".format(
                        searchFor, current_dir
                    )

                result = subprocess.check_output(args, shell=True)
                result = int(result.decode('utf-8'))
                results.append(result)

        return results

    def updateDb(dbConn, py_name, values):
        cur = dbConn.cursor()  # cursor to make changes

        # Replace None values with 'NULL' for Postgres
        values = ['NULL' if value is None else value for value in values]

        sql = ['classCount_{} = {}'.format(item[0], value)
               for item, value in zip(tasks.getSearchItems(), values)]
        sql = str.join(', ', sql)

        sql = "UPDATE project.metadata SET {} WHERE name = '{}';".format(
                    sql, py_name
               )

        cur.execute(sql)
        dbConn.commit()

    def getColumns():
        # TODO Refactor so the whole system uses tuples rather than arrays of
        # length 2
        return [['classCount_' + t[0], 'int'] for t in tasks.getSearchItems()]

    def getSearchItems():
        """Return a list of tuples in the form (search term, search type).

        Type is either xml.tag or xml.class_
        The search type should not be confused with the column type, which is
        usually (or in this module, always) int.
        """
        return [t for k, value in tasks.searchItems.items() for t in value]
