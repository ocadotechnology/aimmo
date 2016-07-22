import os
from setuptest.setuptest import SetupTestSuite
import unittest


class AllTests(SetupTestSuite):
    def __init__(self):
        super(AllTests, self).__init__()
        BASE_DIR = os.path.dirname(__file__)
        APPS = (
            'aimmo-game',
            'aimmo-game-creator',
            'aimmo-game-worker',
        )
        for app in APPS:
            dir = os.path.join(BASE_DIR, app)
            self.addTests(unittest.TestLoader().discover(dir))
            self.packages.append(app)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(AllTests())
