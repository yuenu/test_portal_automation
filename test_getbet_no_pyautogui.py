import unittest
from LoingConfig import PortalLoginConfig, GameHall
import time


class PortalLoginTest(unittest.TestCase):

    def setUp(self):
        self.portal = PortalLoginConfig()

    def tearDown(self):
        self.portal.driver.quit()

    def test_captcha_pass(self):
        self.portal.login()
        time.sleep(3)
        self.GameHall.goAPfishs()
       # self.portal.goGPKfish()
       # self.portal.goAPfish()
       # self.portal.goAEelgame()


if __name__ == "__main__":
    unittest.main()
