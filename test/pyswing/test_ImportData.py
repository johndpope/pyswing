import datetime
import logging
import unittest
import sqlite3

from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
import pyswing.constants
from pyswing.ImportData import importData
from unittest.mock import patch
from pyswing.objects.equity import Equity


class TestImportData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        deleteFile("output/TestImportData.db")

        pyswing.constants.pySwingDatabase = "output/TestImportData.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        Logger.log(logging.INFO, "Creating Test Database", {"scope":__name__, "database":pyswing.constants.pySwingDatabase})
        query = open('resources/pyswing.sql', 'r').read()
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        c.executescript(query)
        connection.commit()
        c.close()
        connection.close()

    @classmethod
    def tearDownClass(self):
        deleteFile("output/TestImportData.db")
        pass


    def test_ImportData(self):

        pretendDate = datetime.datetime(2015, 5, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:
            args = "-n unitTest".split()
            importData(args)

        rowCount = self._countEquityRows()
        self.assertEqual(rowCount, 261) # 87 * 3

        pretendDate = datetime.datetime(2015, 6, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:
            args = "-n unitTest".split()
            importData(args)

        rowCount = self._countEquityRows()
        self.assertEqual(rowCount, 324) # 108 * 3


    def _countEquityRows(self):
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        query = "select count(1) from Equities"
        cursor = connection.cursor()
        cursor.execute(query)
        rowCount = cursor.fetchone()[0]
        connection.close()
        return rowCount


if __name__ == '__main__':
    unittest.main()

