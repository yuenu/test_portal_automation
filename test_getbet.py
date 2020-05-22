import unittest
from LoingConfig import PortalLoginConfig, GameHall
import time


class PortalLoginTest(unittest.TestCase):

    def setUp(self):
        self.portal = PortalLoginConfig()
        self.game = GameHall()

    def tearDown(self):
        self.portal.driver.close()
        self.portal.driver.quit()

    def test_captcha_pass(self):
        self.portal.login()
        time.sleep(3)
        # self.game.goCRsport()
        # self.game.go3singsport()
        # self.game.goSABAsport()

        # self.game.goSYlottery()



        self.game.goFBGelgame()
        # 別種定位
        # self.game.goSGelgame()

        # 電子 - 確認ok
        # self.game.goTOGelgame()
        # self.game.goAEelgame()
        # self.game.goPGelgame()
        # self.game.goSWelgame()
        # self.game.goDTelgame()
        # self.game.goGPKelgame()
        # self.game.goJSelgame()
        # self.game.goGPK2elgame()
        # self.game.goPTelgame()

        # 捕魚 - 確認ok
        # self.game.goAPfish()
        # self.game.goGPKfish()
        # self.game.goFGfish()
        # self.game.goJDBfish()
        # self.game.goLEGfish()
        # self.game.goVGfish()
        # self.game.goMWfish()
        # self.game.goFGbird()
        # self.game.goTHfish()

        # 太花錢
        # self.game.goMTfish()

        # AB007沒有AB005、AB006有的,已ok
        # self.game.goBSPfish()
        # self.game.goICGfish()
        # self.game.goGPK2fish()
        # self.game.goKAfish()


if __name__ == "__main__":
    unittest.main()
