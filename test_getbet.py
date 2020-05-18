import unittest
from LoingConfig import PortalLoginConfig, GameHall
import time


class PortalLoginTest(unittest.TestCase):

    def setUp(self):
        self.portal = PortalLoginConfig()
        self.game = GameHall()

    def tearDown(self):
        self.portal.driver.quit()

    def test_captcha_pass(self):
        self.portal.login()
        time.sleep(3)
        # self.game.goSWelgame()
        self.game.goAPfish()
        # self.game.goFGfish()
        # self.game.goPGelgame()
        # self.game.goAPfish()
        # self.game.goGPKfish()
        # self.game.goFGbird()
        # self.game.goSYlottery()

if __name__ == "__main__":
    unittest.main()
