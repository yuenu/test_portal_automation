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
        # self.game.goCRsport()
        # self.game.go3singsport()
        # self.game.goSABAsport()

        # 樂透
        # self.game.goSYlottery()
        #
        # # 電子
        # self.game.goPGelgame()
        # self.game.goSWelgame()
        # self.game.goAEelgame()
        # self.game.goDTelgame()

        # 捕魚
        # self.game.goGPKfish()
        # self.game.goFGfish()
        # self.game.goFGbird()
        # self.game.goAPfish()
        # self.game.goLEGfish()
        # self.game.goMTfish()
        # self.game.goMWfish()
        # self.game.goVGfish()
        # self.game.goBSPfish()
        # self.game.goYGfish()
        # self.game.goJDBfish()
        # self.game.goGPK2fish()
        # self.game.goTHfish()
        self.game.goKAfish()



if __name__ == "__main__":
    unittest.main()
