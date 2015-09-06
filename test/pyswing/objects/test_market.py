import unittest

from utils.FileHelper import forceWorkingDirectory
from utils.Logger import Logger
from pyswing.objects.market import Market


class TestMarket(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        self._market = Market("resources/asx.txt")

    @classmethod
    def tearDown(self):
        pass


    def test_tickers(self):

        self.assertEqual(len(self._market.tickers.index), 72)

        # for index, row in self._market.tickers.iterrows():
        #     print(row[0])


if __name__ == '__main__':
    unittest.main()
