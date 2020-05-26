import unittest
from LoingConfig import PortalLoginConfig, GameHall, UserSimulation
import time


class PortalLoginTest(unittest.TestCase):

    def setUp(self):
        self.portal = PortalLoginConfig()
        self.game = GameHall()
        self.user = UserSimulation()

    def tearDown(self):
        self.portal.driver.close()
        self.portal.driver.quit()

    def test_captcha_pass(self):
        self.portal.login()
        time.sleep(3)
        #self.user.BetRecoed()
        self.user.Deposit()
        self.user.Transaction()
        self.user.WithdrawApplication()
        self.user.SecurityList_sendEmail()



        # 體育(暫緩，串關定位要研究)
        # self.game.go3singsport()
        # self.game.goSABAsport()

        # 彩票 - 確認ok
        # self.game.goSYlottery()
        # self.game.goIGlottery()

        # 別種定位 , 複雜定位  目前解決不了
        # self.game.goSGelgame()
        # self.game.goFBGelgame()

        # 電子 - 確認ok
        # self.game.goTOGelgame()
        # self.game.goAEelgame()
        # self.game.goPGelgame()
        # self.game.goSWelgame()
        # self.game.goDTelgame()
        # self.game.goGPK2elgame()
        # self.game.goJSelgame()
        # self.game.goPTelgame()
        # self.game.goJDBelgame()
        # self.game.goHBelgame()
        # self.game.goSYelgame()
        # self.game.goFGargame()
        # self.game.goGPKelgame()
        # self.game.goKAelgame()

        # 捕魚 - 確認ok
        # self.game.goAPfish()
        # self.game.goGPKfish()
        # self.game.goFGfish()
        # self.game.goJDBfish()
        # self.game.goLEGfish()
        # self.game.goVGfish()
        # self.game.goMWfish()
        # self.game.goFGbird()
        # self.game.goMTfish()
        # self.game.goTHfish()

        # AB007沒有AB005、AB006有的,已ok
        # self.game.goBSPfish()
        # self.game.goICGfish()
        # self.game.goGPK2fish()
        # self.game.goKAfish()


if __name__ == "__main__":
    unittest.main()
