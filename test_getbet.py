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
        self.portal.goAEelgame()
        self.portal.goAPfish()
        self.portal.goGPKfish()
        self.portal.goFGbird()

if __name__ == "__main__":
    unittest.main()
