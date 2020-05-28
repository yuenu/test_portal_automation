import unittest
from LoingConfig import PortalLoginConfig, GameHall, UserSimulation ,entergmae
import time
import random


class PortalLoginTest(unittest.TestCase):


    def setUp(self):
        self.portal = PortalLoginConfig()
        self.game = GameHall()
        self.user = UserSimulation()
        self.entergame = entergmae()

    def tearDown(self):
        self.portal.driver.close()
        self.portal.driver.quit()

    def test_captcha_pass(self):
        self.portal.login()
        time.sleep(2)
        all_list = []
        usersimulation_list = [
            'self.user.SecurityList_sendEmail()',
            'self.user.WithdrawApplication()',
            'self.user.Deposit()',
            'self.user.BetRecoed()',
            'self.user.Transaction()',
            'self.user.updatingBalance()',
        ]
        game_list = [
            'self.game.goAEelgame()',
            'self.game.goSWelgame()',
            'self.game.goJSelgame()',
            'self.game.goHBelgame()',
            'self.game.goAPfish()',
            'self.game.goFGbird()',
            'self.game.goGPKfish()',
            'self.game.goVGfish()',
            'self.game.goLEGfish()',
            'self.game.goIGlottery()',
            'self.game.goICGfish()',
            'self.game.goKAfish()',
            'self.game.goBSPfish()',
        ]
        entergame_list = [
            'self.entergame.enterGPKfish()',
            'self.entergame.enterRMboard()',
            'self.entergame.enterGPKboard()',
            'self.entergame.enterDTboard()',
            'self.entergame.enterAPboard()',
            'self.entergame.enterVGboard()',
            'self.entergame.enterFSboard()',
            'self.entergame.enterTOGboard()',
            'self.entergame.enterNWboard()',
            'self.entergame.enterMWboard()',
            'self.entergame.enterJSboard()',
            'self.entergame.enterLEGboard()',
            'self.entergame.enterJDBboard()',
            'self.entergame.enterGMGboard()',
            'self.entergame.enterMTboard()',
            'self.entergame.enterSYboard()',
            'self.entergame.enterTHboard()',
            'self.entergame.enterGPKfish()',
            'self.entergame.enterAPfish()',
            'self.entergame.enterJDBfish()',
            'self.entergame.enterFGfish()',
            'self.entergame.enterPSfish()',
            'self.entergame.enterTHfish()',
            'self.entergame.enterLEGfish()',
            'self.entergame.enterMTfish()',
            'self.entergame.enterVGfish()',
            'self.entergame.enterR8fish()',
            'self.entergame.enterBBINlive()',
            'self.entergame.enterAGlive()',
            'self.entergame.enterPTlive()',
            'self.entergame.enterMGlive()',
            'self.entergame.enterABlive()',
            'self.entergame.enterEVOlive()',
            'self.entergame.enterGDlive()',
            'self.entergame.enterGPKlive()',
            'self.entergame.enterSBlive()',
            'self.entergame.enterOGlive()',

        ]
        # user_times = random.randint(1, 4)
        # user_randomlist = random.sample(usersimulation_list, user_times)
        #
        # game_times = random.randint(1, 2)
        # game_randomlist = random.sample(game_list, game_times)
        #
        # entergame_times = random.randint(0, 1)
        # entergame_randomlist = random.sample(entergame_list, entergame_times)
        #
        # all_list.extend(user_randomlist)
        # all_list.extend(game_randomlist)
        # all_list.extend(entergame_randomlist)
        # print('all_list:', all_list)
        # random.shuffle(all_list)
        # print('random all_list:', all_list)
        # for dothing in all_list:
        #     eval(dothing)

        #  UserSimulation
        # self.user.BetRecoed()
        # self.user.Deposit()
        # self.user.Transaction()
        self.user.WithdrawApplication()
        # self.user.SecurityList_sendEmail()

        # 彩票 - 確認ok
        # self.game.goSYlottery()
        # self.game.goIGlottery()

        # 體育(暫緩，串關定位要研究)
        # self.game.go3singsport()
        # self.game.goSABAsport()

        # 電子 - 確認ok
        # self.game.goPGelgame() # 待修
        # self.game.goTOGelgame()
        # self.game.goAEelgame()
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
        # self.game.goICGfish()
        # self.game.goKAfish()
        # self.game.goBSPfish()

if __name__ == "__main__":
    unittest.main()




# 體育(暫緩，串關定位要研究)
# self.game.go3singsport()
# self.game.goSABAsport()

# 彩票 - 確認ok
# self.game.goSYlottery()
# self.game.goIGlottery()

# 別種定位 , 複雜定位  目前解決不了
# self.game.goSGelgame()
# self.game.goFBGelgame()


# AB007沒有AB005、AB006有的,已ok
# self.game.goGPK2fish()





        #  UserSimulation
        # self.user.BetRecoed()
        # # self.user.Deposit()
        # # self.user.Transaction()
        # # self.user.WithdrawApplication()
        # self.user.SecurityList_sendEmail()

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

