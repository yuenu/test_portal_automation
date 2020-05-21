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

        # self.game.goPGelgame()
        # self.game.goSWelgame()
        # self.game.goAEelgame()
        # self.game.goDTelgame()
        #self.game.goSGelgame()
        self.game.goTOGelgame()




        # 待確認 self.game.goMWfish()


        # self.game.goBSPfish()
        # self.game.goGPK2fish()
        # self.game.goKAfish()

        # self.game.goAPfish()
        # self.game.goGPKfish()
        # self.game.goJDBfish()
        # self.game.goLEGfish()
        # self.game.goMTfish()
        # self.game.goVGfish()
        # self.game.goFGfish()
        # self.game.goFGbird()
        # self.game.goTHfish()

if __name__ == "__main__":
    unittest.main()
