import unittest
from capabilities import grepEntries


class TestGrepEntries(unittest.TestCase):

    def test_grep_analyze(self):
        tasks = grepEntries.tasks

        results = tasks.analyze('data/testlangproj-ih-flex')

        # These values are in the current order returned by grepEntries
        # To verify they are correct it is necessary to manually inspect the
        # example FLEx project in the repo.
        true_results = [64, 66, 2, 0, 0, 6, 3, 10, 2, 3, 26, 0, 693, 704, 5,
                        1910, 85, 0, 10, 5, 0, 0, 0]

        # Columns pairs field names with their data types
        columns = tasks.getColumns()

        for x, y, z in zip(results, true_results, columns):
            msg = 'Count for {} should be {} but was {}'.format(z[0], y, x)
            self.assertEqual(x, y, msg)


if __name__ == '__main':
    unittest.main()
