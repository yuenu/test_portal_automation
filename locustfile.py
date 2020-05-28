import random
from locust import HttpUser, task, between
from test_loginaction import PortalLoginTest

class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    def on_start(self):
        self.Test = PortalLoginTest()

    @task
    def index_page(self):
        self.Test.test_captcha_pass()