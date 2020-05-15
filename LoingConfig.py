import time
import base64
import pytesseract
from bs4 import BeautifulSoup
from selenium import webdriver
from idenitfy import idenitfy_img
from selenium.webdriver import ActionChains

pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract.exe'


class PortalLoginConfig(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.windowSize = self.driver.set_window_size(1080, 800)
        self.account = 'yuenu001'
        self.password = 's24930479'
        self.filepath = f'./recaptcha/captcha.png'

    def isAnnuncement(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        announcement_element = soup.select('div.show#marquee-wrapper')
        announcement2 = soup.find_all(class_='modal-overlay modal-show')
        time.sleep(2.5)
        if len(announcement_element) != 0:
            self.driver.find_element_by_xpath('//*[@id="marquee"]/footer/span').click()
        else:
            print('None announcement')

        if len(announcement2) != 0:
            self.driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/i').click()


    def sendUserInfo(self, account, password):
        time.sleep(0.5)
        self.driver.find_element_by_id('login_account').send_keys(self.account)
        self.driver.find_element_by_id('login_password').send_keys(self.password)

    def parsingPageSourceAndSaveImageSendCode(self, filepath):
        self.driver.find_element_by_css_selector('#login_code').click()
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        imgstring = soup.select('#captcha')[0].get('ng-src')[22:]
        imgdata = base64.b64decode(imgstring)
        with open(self.filepath, 'wb') as f:
            f.write(imgdata)

        captcha_code = idenitfy_img(self.filepath)
        if len(captcha_code) == 4:
            self.driver.find_element_by_css_selector('#login_code').send_keys(captcha_code)
        else:
            print('The cpatcha_code < 4')
            self.driver.find_element_by_css_selector('#login_code').send_keys('0000')

    def clickLoginIn(self):
        self.driver.find_element_by_css_selector('#login-box').click()
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        device_verification = soup.select('i.fas.fa-times-circle.close')
        # 裝置驗證彈窗辨識
        print(len(device_verification))
        if len(device_verification) != 0:
            self.driver.find_element_by_class_name('fas.fa-times-circle.close').click()
        else:
            pass
        self.isAnnuncement()

    def loginFail(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        time.sleep(1)
        alert = soup.find_all(class_='custom-modal')
        if len(alert) > 0:
            for i in range(10):
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                alert = soup.find_all(class_='custom-modal')
                if len(alert) > 0:
                    button = self.driver.find_element_by_xpath('/html/body/div[12]/div/div/div[3]/button[2]')
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(1.5)
                    self.parsingPageSourceAndSaveImageSendCode(self.filepath)
                    self.clickLoginIn()
                    time.sleep(2)
                else:
                    break
        else:
            pass

    def login(self):
        self.driver.get('http://www.fnjtd.com/')
        self.isAnnuncement()
        self.sendUserInfo(self.account, self.password)
        self.parsingPageSourceAndSaveImageSendCode(self.filepath)
        self.clickLoginIn()
        self.loginFail()

    def logout(self):
        self.driver.get('http://www.fnjtd.com/Account/SignOut')

    def goAPfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        AP_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[3]/li[5]')  # AP金蟾捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(AP_fish).perform()
        time.sleep(12)
        windows = self.driver.window_handles  # 獲得當前瀏覽器所有視窗
        self.driver.switch_to.window(windows[-1])  # 切換至最新彈窗
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform() # 點擊0.1元炮場
        time.sleep(4)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.5)
        time.sleep(10)

    def goGPKfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        GPK_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[2]/li[1]')  # GPK王者捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(GPK_fish).perform()
        time.sleep(12)
        windows = self.driver.window_handles  # 獲得當前瀏覽器所有視窗
        self.driver.switch_to.window(windows[-1])  # 切換至最新彈窗
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(200, 150).click().perform()  # 點擊0.1元炮場
        time.sleep(4)

        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.5)
        time.sleep(10)

    def goAEelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        AEelgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/div/ol[1]/li[6]')  # AE阿米巴电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(AEelgame).perform()
        time.sleep(8)
        windows = self.driver.window_handles  # 獲得當前瀏覽器所有視窗
        self.driver.switch_to.window(windows[-1])  # 切換至最新彈窗
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(400, 520).click().perform()  # 案"一路發"
        windows = self.driver.window_handles  # 獲得當前瀏覽器所有視窗
        self.driver.switch_to.window(windows[-1])  # 切換至最新彈窗
        time.sleep(5)
        ActionChains(self.driver).move_by_offset(-200, -200).click().perform()
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(2)
        time.sleep(5)

    def goSYlottery(self):
        lobby_lottery = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[7]/a')  # "彩票游戏"下拉式選單
        SY_lotery = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[7]/ol/li[8]')  # SY双赢彩票
        ActionChains(self.driver).move_to_element(lobby_lottery).click(SY_lotery).perform()
        time.sleep(8)
        windows = self.driver.window_handles  # 獲得當前瀏覽器所有視窗
        self.driver.switch_to.window(windows[-1])  # 切換至最新彈窗
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(200, 150).click().perform()  # 點擊0.1元炮場
        time.sleep(4)

        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.5)
        time.sleep(10)


class GameHall(PortalLoginConfig):

    def __init__(self):
        super(GameHall, self).__init__()

    def goAPfishs(self):
        fish_btn = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')
        # GPK_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[2]/li[1]')
        AP_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[3]/li[5]')
        ActionChains(self.driver).move_to_element(fish_btn).click(AP_fish).perform()
        time.sleep(10)
        windows = self.driver.window_handles  # 獲得當前瀏覽器所有視窗
        self.driver.switch_to.window(windows[-1])  # 切換至最新彈窗
        time.sleep(2)
        # 點擊0.1元炮場
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(4)
        # 發炮
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(0.5)
        # 發炮2
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()