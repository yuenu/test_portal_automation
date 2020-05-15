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
        self.portal.goAEelgame()
        time.sleep(3)
        self.portal.goAPfish()
        time.sleep(3)
        self.portal.goGPKfish()
        time.sleep(3)
        self.portal.goJDBfish()
        time.sleep(3)

if __name__ == "__main__":
    unittest.main()
