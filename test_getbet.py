import unittest
from LoingConfig import PortalLoginConfig
import time


class PortalLoginTest(unittest.TestCase):

    def setUp(self):
        self.portal = PortalLoginConfig()

    def tearDown(self):
        self.portal.driver.quit()

    def test_captcha_pass(self):
        self.portal.login()
        time.sleep(3)

        self.portal.goFGfish()
        time.sleep(5)
        self.portal.goAEelgame()
        time.sleep(3)
        self.portal.goAPfish()
        time.sleep(3)
        self.portal.goGPKfish()
        time.sleep(3)
        self.portal.goFGbird()
        time.sleep(3)

if __name__ == "__main__":
    unittest.main()
