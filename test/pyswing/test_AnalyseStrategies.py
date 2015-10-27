import datetime
import unittest
import sqlite3

from utils.FileHelper import forceWorkingDirectory, deleteFile, copyFile
from utils.Logger import Logger
import pyswing.constants
import pyswing.globals
from pyswing.EvaluateTwoRuleStrategies import evaluateTwoRuleStrategies
from pyswing.EvaluateThreeRuleStrategies import evaluateThreeRuleStrategies
from pyswing.AnalyseStrategies import analyseStrategies


class TestAnalyseStrategies(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.constants.pySwingDatabase = "output/TestAnalyseStrategies.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        copyFile(pyswing.constants.pySwingTestDatabase, pyswing.constants.pySwingDatabase)

    @classmethod
    def tearDownClass(self):
        # deleteFile(pyswing.constants.pySwingDatabase)
        pass


    def test_AnalyseStrategies(self):

        args = "-n unitTest -m 0.1 -s test_EvaluateTwoRuleStrategies".split()
        evaluateTwoRuleStrategies(args)

        rowCount = self._countRows("TwoRuleStrategy")

        self.assertEqual(rowCount, 4872)

        args = "-n unitTest -N 1 -s v4.0 -t 5".split()
        evaluateThreeRuleStrategies(args)

        rowCount = self._countRows("ThreeRuleStrategy")

        self.assertEqual(rowCount, 53)

        args = "-n unitTest -r 5.0 -s v4.0 -t 4".split()
        analyseStrategies(args)

        rowCount = self._countRows("Strategy")

        self.assertEqual(rowCount, 1)


    def _countRows(self, tableName):
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        query = "select count(1) from '%s'" % (tableName)
        cursor = connection.cursor()
        cursor.execute(query)
        rowCount = cursor.fetchone()[0]
        connection.close()
        return rowCount


if __name__ == '__main__':
    unittest.main()

