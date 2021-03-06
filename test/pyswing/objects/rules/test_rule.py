import unittest

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.objects.rules.rule import Rule, getRules
import pyswing.constants
import pyswing.database
from pyswing.CreateDatabase import createDatabase


class TestRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.database.overrideDatabase("output/TestRule.db")

        args = "-n %s" % ("unitTesting")
        createDatabase(args.split())

        myRule = Rule("Rule - myRule")
        myRule._createTable()

        myOtherRule = Rule("Rule - myOtherRule")
        myOtherRule._createTable()

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.database.pySwingDatabase)


    def test_CrossingRule(self):

        rules = getRules()

        self.assertTrue(any("Rule - myRule" in rule for rule in rules))
        self.assertTrue(any("Rule - myOtherRule" in rule for rule in rules))
        self.assertFalse(any("Rule - onlyJoking" in rule for rule in rules))


if __name__ == '__main__':
    unittest.main()
