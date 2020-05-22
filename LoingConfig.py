import time
import base64
import pytesseract
from bs4 import BeautifulSoup
from selenium import webdriver
from idenitfy import idenitfy_img
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract.exe'


class PortalLoginConfig(object):
    driver = webdriver.Chrome()
    driver.set_window_size(1080, 800)
    driver.get('http://www.jp777.net/')
    '''
    AB005 - http://www.fnjtd.com/
    AB006 - http://www.rfben.com/
    AB007 - http://www.jp777.net/
    '''
    def __init__(self):
        self.account = 'QATest0'
        self.password = 'a123456'
        self.filepath = f'./recaptcha/captcha.png'

    def isAnnuncement(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        announcement_element = soup.select('div.show#marquee-wrapper')
        announcement2 = soup.find_all(class_='modal-overlay modal-show')
        time.sleep(3)
        if len(announcement_element) != 0:
            self.driver.find_element_by_xpath('//*[@id="marquee"]/footer/span').click()
        else:
            print('None announcement')

        if len(announcement2) != 0:
            self.driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/i').click()

    def device_verification(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        device_verification = soup.select('i.fas.fa-times-circle.close')
        # 裝置驗證彈窗辨識
        print(len(device_verification))
        if len(device_verification) != 0:
            self.driver.find_element_by_class_name('fas.fa-times-circle.close').click()
        else:
            pass


    def sendUserInfo(self, account, password):
        time.sleep(1)
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
        self.device_verification()
        self.isAnnuncement()

    def loginFail(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        time.sleep(1)
        alert = soup.find_all(class_='custom-modal')
        valid = soup.select("#cms-modal-input")
        if len(alert) == 1 or len(valid) == 1:
            print('valid:', valid)
            for i in range(10):
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                alert = soup.find_all(class_='custom-modal')
                valid = soup.select("#cms-modal-input")
                if len(alert) == 1 and len(valid) == 0:
                    print('驗證碼錯誤')
                    button = self.driver.find_element_by_xpath('/html/body/div[12]/div/div/div[3]/button[2]')
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(1.5)
                    self.parsingPageSourceAndSaveImageSendCode(self.filepath)
                    self.clickLoginIn()
                    time.sleep(2)

                elif len(alert) == 1 and len(valid) == 1:
                    print('跨區驗證')
                    time.sleep(0.5)
                    self.driver.find_element_by_xpath('//*[@id="cms-modal-input"]').send_keys('123456')
                    time.sleep(0.5)
                    self.driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[12]/div/div/div[3]/button[2]').click()
                    time.sleep(5)
                    self.device_verification()
                    self.isAnnuncement()
                else:
                    break
        else:
            pass

    def login(self):
        self.isAnnuncement()
        self.sendUserInfo(self.account, self.password)
        self.parsingPageSourceAndSaveImageSendCode(self.filepath)
        self.clickLoginIn()
        self.loginFail()
        time.sleep(2)

    def logout(self):
        self.driver.get('http://www.fnjtd.com/Account/SignOut')

    def switch_window(self):
        windows = self.driver.window_handles  # 獲得當前瀏覽器所有視窗
        self.driver.switch_to.window(windows[-1])  # 切換至最新彈窗

    def switch_iframe(self):
        frame = self.driver.find_element_by_css_selector('iframe')
        self.driver.switch_to.frame(frame)


class GameHall(PortalLoginConfig):

    # """捕鱼游戏"""
    def goAPfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        AP_fish = self.driver.find_element_by_css_selector('[game-box="ap-jinchan"]')  # AP金蟾捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(AP_fish).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(1)
        canvas = self.driver.find_element_by_id('layaCanvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 600, 300).click().perform()  # 點擊0.1元炮場
        time.sleep(6)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
        time.sleep(8)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goFGbird(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        FG_bird = self.driver.find_element_by_css_selector('[game-box="fg-bird"]')
        ActionChains(self.driver).move_to_element(lobby_fish).click(FG_bird).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(1)
        canvas = self.driver.find_element_by_id('GameCanvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 235, 335).click().perform()  # 點擊0.1元炮場
        time.sleep(4)
        for j in range(5):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goFGfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        FG_fish = self.driver.find_element_by_css_selector('[game-box="fg-beauty"]')  # FG美人捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(FG_fish).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(2)
        canvas = self.driver.find_element_by_id('GameCanvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 250, 400).click().perform()  # 點擊0.1元炮場
        time.sleep(5)
        ActionChains(self.driver).move_by_offset(830, -370).click().perform()  # Close "x"
        for j in range(5):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
        time.sleep(8)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goGPKfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        GPK_fish = self.driver.find_element_by_css_selector('[game-box="gpk-monopoly"]')  # GPK王者捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(GPK_fish).perform()
        time.sleep(10)
        self.switch_window()
        time.sleep(1)
        canvas = self.driver.find_element_by_id('layaCanvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 250, 400).click().perform()  # 點擊0.1元炮場
        time.sleep(8)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
        time.sleep(8)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goGPK2fish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        GPK2_fish = self.driver.find_element_by_css_selector('[game-box="gpk2-fish"]')  # GPK2大圣降魔
        ActionChains(self.driver).move_to_element(lobby_fish).click(GPK2_fish).perform()
        time.sleep(18)
        self.switch_window()
        time.sleep(1)
        canvas = self.driver.find_element_by_id('view')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 1000, 650).click().perform()  # 點擊進入遊戲
        time.sleep(3)
        ActionChains(self.driver).move_by_offset(-500, -300).click().perform()  # 點擊0.01
        time.sleep(8)
        for j in range(50):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goJDBfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        JDB_fish = self.driver.find_element_by_css_selector('[game-box="jdb-dragon"]')  # JDB龙王捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(JDB_fish).perform()
        time.sleep(14)
        self.switch_window()
        time.sleep(1)
        canvas = self.driver.find_element_by_id('StageDelegateDiv')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 400, 300).click().perform()  # 點擊0.1元炮場
        time.sleep(4)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(5)

    # TH捕魚關閉的話不會馬上把錢轉出來，後面有皆其他娛樂城的話不會帶錢進去
    def goTHfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        TH_fish = self.driver.find_element_by_css_selector('[game-box="th-toad"]')  # TH金蟾捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(TH_fish).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(2)
        canvas = self.driver.find_element_by_id('StageDelegateDiv')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 600, 350).click().perform()  # 點擊0.1元炮場
        time.sleep(5)
        for j in range(70):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(8)

    def goLEGfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        LEG_fish = self.driver.find_element_by_css_selector('[game-box="leg-fish"]')  # LEG捕鱼大作战
        ActionChains(self.driver).move_to_element(lobby_fish).click(LEG_fish).perform()
        time.sleep(10)
        self.switch_window()
        time.sleep(2)
        canvas = self.driver.find_element_by_id('StageDelegateDiv')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 250, 400).click().perform()  # 點擊0.1元炮場
        time.sleep(5)
        ActionChains(self.driver).move_by_offset(975, 215).click().perform()  # 自動射擊
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(5)

    '''MV捕魚花錢可能會比較多一點,一發1元'''
    def goMTfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        MT_fish = self.driver.find_element_by_css_selector('[game-box="mt-lee"]')  # MT美天李逵劈鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(MT_fish).perform()
        time.sleep(15)
        self.switch_window()
        time.sleep(2)
        canvas = self.driver.find_element_by_id('layaCanvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 250, 450).click().perform()  # 點擊0.1元炮場
        time.sleep(11)
        ActionChains(self.driver).move_by_offset(885, -340).click().perform()  # 點"x"
        time.sleep(1)
        for j in range(2):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goMWfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        MW_fish = self.driver.find_element_by_css_selector('[game-box="mw-fish"]')  # MW千炮捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(MW_fish).perform()
        time.sleep(22)
        self.switch_window()
        time.sleep(2)
        canvas = self.driver.find_element_by_id('StageDelegateDiv')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 200, 250).click().perform()  # 點擊0.1元炮場
        time.sleep(15)
        ActionChains(self.driver).move_by_offset(450, 140).click().perform()  # 點"確定"
        time.sleep(1)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 點擊
            time.sleep(2)
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goVGfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        VG_fish = self.driver.find_element_by_css_selector('[game-box="vg-fish"]')  # VG龙王捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(VG_fish).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(2)
        canvas = self.driver.find_element_by_id('StageDelegateDiv')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 270, 500).click().perform()  # 點擊0.1元炮場
        time.sleep(7)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
        time.sleep(6)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goBSPfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        BSP_fish = self.driver.find_element_by_css_selector('[game-box="bsp-fishcannon"]')  # BSP千炮捕鱼王3D
        ActionChains(self.driver).move_to_element(lobby_fish).click(BSP_fish).perform()
        time.sleep(10)
        self.switch_window()
        time.sleep(2)
        canvas = self.driver.find_element_by_css_selector('.home')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 1100, 150).click().perform()  # 'x'
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(-800, 250).click().perform()  # 點擊0.1元炮場
        time.sleep(10)
        ActionChains(self.driver).move_by_offset(280, 400).click().perform()  # 點擊自動
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goICGfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        ICG_fish = self.driver.find_element_by_css_selector('[game-box="icg-fish"]')  # ICG龙珠捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(ICG_fish).perform()
        time.sleep(10)
        self.switch_window()
        time.sleep(2)
        canvas = self.driver.find_element_by_id('GameCanvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 250, 400).click().perform()  # '0.01炮場'
        time.sleep(10)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    '''YG 捕鱼进行系统维护中 .......'''
    # def goYGfish(self):
    #     lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
    #     goYGfish = self.driver.find_element_by_css_selector('[game-box="yg-fishseaking"]')  # YG超级海王
    #     ActionChains(self.driver).move_to_element(lobby_fish).click(goYGfish).perform()
    #     time.sleep(10)
    #     self.switch_window()
    #     time.sleep(2)
    #     ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 點擊0.1元炮場
    #     time.sleep(2)
    #     ActionChains(self.driver).move_by_offset(115, 225).click().perform()  # 點擊自動
    #     time.sleep(2)
    #     ActionChains(self.driver).move_by_offset(0, 0).click().perform()
    #     time.sleep(8)
    #     self.driver.close()
    #     self.switch_window()
    #     time.sleep(3)

    def goKAfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        goKAfish = self.driver.find_element_by_css_selector('[game-box="ka-fish"]')  # KA爽爽捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(goKAfish).perform()
        time.sleep(13)
        self.switch_window()
        time.sleep(1)
        canvas = self.driver.find_element_by_id('GameCanvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 250, 400).click().perform()  # '0.01炮
        time.sleep(5)
        ActionChains(self.driver).move_by_offset(1000, 0).click().perform() # 點擊自動射擊
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # click dou dou
        time.sleep(6)
        self.driver.close()
        self.switch_window()
        time.sleep(3)


    '''
    电子游艺 (AB005)
    '''
    def goAEelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        AE_elgame = self.driver.find_element_by_css_selector('[ng-click="toAeHtml()"]')  # AE阿米巴电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(AE_elgame).perform()
        time.sleep(7)
        self.switch_window()
        self.switch_iframe()
        time.sleep(1)
        self.driver.find_element_by_css_selector('[title="一本万利"]').click()
        time.sleep(8)
        self.switch_window()
        self.switch_iframe()
        canvas = self.driver.find_element_by_id('gameDiv')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 210, 640).click().perform()
        for i in range(4):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 3 確定
            time.sleep(0.3)
        ActionChains(self.driver).move_by_offset(425, 0).click().perform()  # 3 確定
        for j in range(2):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(5)
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goPGelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        PG_elgame = self.driver.find_element_by_css_selector('[ng-click="toJtnHtml()"]')  # PG电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(PG_elgame).perform()
        time.sleep(6)
        self.switch_window()
        self.switch_iframe()
        time.sleep(1)
        self.driver.find_element_by_css_selector('[title="冰雪大冲关"]').click()
        time.sleep(8)
        self.switch_window()
        self.switch_iframe()
        canvas = self.driver.find_element_by_id('Cocos2dGameContainer')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 640, 660).click().perform()  # 開始
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(-110, 110).click().perform()  # "減碼按鈕"
        for j in range(8):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        ActionChains(self.driver).move_by_offset(100, 0).click().perform()  # "轉動按鈕"
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(4)
        time.sleep(8)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    #  定位法較特別，暫緩
    # def goSGelgame(self):
    #     lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
    #     SG_elgame = self.driver.find_element_by_css_selector('[ng-click="toSgFlash()"]')  # SG电子游艺
    #     ActionChains(self.driver).move_to_element(lobby_elgame).click(SG_elgame).perform()
    #     time.sleep(8)
    #     self.switch_window()
    #     self.switch_iframe()
    #     time.sleep(1)
    #     self.driver.find_element_by_css_selector('[title="金鸡"]').click()
    #     time.sleep(8)
    #     self.switch_window()
    #     self.switch_iframe()
    #     canvas = self.driver.find_element_by_id('controlbarH5')
    #     ActionChains(self.driver).move_to_element_with_offset(canvas, 200, 730).click().perform()  # "減碼按鈕"
    #     for j in range(8):
    #         ActionChains(self.driver).move_by_offset(0, 0).click().perform()
    #     ActionChains(self.driver).move_by_offset(920, 0).click().perform()  # "轉動按鈕"
    #     for j in range(2):
    #         ActionChains(self.driver).move_by_offset(0, 0).click().perform()
    #         time.sleep(4)
    #     time.sleep(8)
    #     self.driver.close()
    #     self.switch_window()
    #     time.sleep(3)

    def goSWelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        SW_elgame = self.driver.find_element_by_css_selector('[ng-click="toPtsHtml()"]')  # 天风电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(SW_elgame).perform()
        time.sleep(6)
        self.switch_window()
        self.switch_iframe()
        self.driver.find_element_by_css_selector('[title="天上凤凰"]').click()
        time.sleep(20)
        self.switch_window()
        self.switch_iframe()
        canvas = self.driver.find_element_by_id('canvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 640, 650).click().perform()  # "減碼按鈕"
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(-325, 50).click().perform()  # "減碼按鈕"
        for j in range(10):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        ActionChains(self.driver).move_by_offset(800, 0).click().perform()  # "轉動按鈕"
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(4)
        time.sleep(6)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goDTelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        DT_elgame = self.driver.find_element_by_css_selector('[ng-click="toDtHtml()"]')  # DT梦想电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(DT_elgame).perform()
        time.sleep(8)
        self.switch_window()
        self.switch_iframe()
        self.driver.find_element_by_css_selector('[title="武松传"]').click()  # 武松传
        time.sleep(15)
        self.switch_window()
        self.switch_iframe()
        canvas = self.driver.find_element_by_id('gameCanvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 230, 685).click().perform() # '-注'
        for i in range(10):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        ActionChains(self.driver).move_by_offset(-195, 0).click().perform()  # '-數'
        for j in range(24):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(1165, 0).click().perform()  # 旋轉
        for k in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(5)
        time.sleep(6)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goTOGelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        TOG_elgame = self.driver.find_element_by_css_selector('[ng-click="toTogHtml()"]')  # TOG星球电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(TOG_elgame).perform()
        time.sleep(6)
        self.switch_window()
        self.switch_iframe()
        time.sleep(1)
        self.driver.find_element_by_css_selector('[title="大闹天宫"]').click()  # 大闹天宫
        time.sleep(20)
        self.switch_window()
        self.switch_iframe()
        canvas = self.driver.find_element_by_id('GameLauncher')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 835, 720).click().perform()  # 籌碼
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(-147, -90).click().perform()  # '-'數
        for i in range(5):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(0.2)
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(450, 80).click().perform()  # 轉動開始
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goGPKelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        GPK_elgame = self.driver.find_element_by_css_selector('[ng-click="toGpkSlot()"]')  # GPK电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(GPK_elgame).perform()
        time.sleep(5)
        self.switch_window()
        self.switch_iframe()
        time.sleep(1)
        self.driver.find_element_by_css_selector('[title="秦皇传说"]').click()  # 秦皇传说
        time.sleep(15)
        self.switch_window()
        self.switch_iframe()
        canvas = self.driver.find_element_by_id('GameCanvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 1140, 120).click().perform()  # 'x'
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(-700, 560).click().perform()  # 押注
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(150, -70).click().perform()  # 1
        ActionChains(self.driver).move_by_offset(600, 0).click().perform()  # 開始
        time.sleep(6)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goGPK2elgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        GPK2_elgame = self.driver.find_element_by_css_selector('[ng-click="toGpk2Html()"]')  # 战游电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(GPK2_elgame).perform()
        time.sleep(5)
        self.switch_window()
        self.switch_iframe()
        time.sleep(1)
        self.driver.find_element_by_css_selector('[title="海底世界"]').click()
        time.sleep(15)
        self.switch_window()
        self.switch_iframe()
        self.switch_iframe()
        canvas = self.driver.find_element_by_id('GTSLOT0030')
        time.sleep(2)
        ActionChains(self.driver).move_to_element_with_offset(canvas, 640, 674).click().perform()  # '確認'
        time.sleep(1)

        ActionChains(self.driver).move_by_offset(-200, 0).click().perform()
        for i in range(5):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        ActionChains(self.driver).move_by_offset(800, 0).click().perform()  # 開始
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(6)
        time.sleep(6)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goJSelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        JS_elgame = self.driver.find_element_by_css_selector('[ng-click="toJsHtml()"]')  # JS金龙电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(JS_elgame).perform()
        time.sleep(5)
        self.switch_window()
        self.switch_iframe()
        time.sleep(1)
        self.driver.find_element_by_css_selector('[title="水果机"]').click()
        time.sleep(12)
        self.switch_window()
        self.switch_iframe()
        canvas = self.driver.find_element_by_id('GameCanvas')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 700, 400).click().perform()  # '新手'
        time.sleep(8)
        ActionChains(self.driver).move_by_offset(270, 180).click().perform()
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(-155, -235).click().perform()
        time.sleep(15)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goPTelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        PT_elgame = self.driver.find_element_by_css_selector('[ng-click="toPtFlash()"]')  # PT电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(PT_elgame).perform()
        time.sleep(5)
        self.switch_window()
        self.switch_iframe()
        time.sleep(1)
        self.driver.find_element_by_css_selector('[title="招财进宝彩池游戏"]').click()
        time.sleep(12)
        self.switch_window()
        for x in range(3):
            if len(self.driver.find_elements_by_css_selector('#messageBoxButtonYes')) == 1:
                messageBoxButton = self.driver.find_element_by_css_selector('#messageBoxButtonYes')
                ActionChains(self.driver).move_to_element(messageBoxButton).click().perform()
                time.sleep(1)
        self.switch_iframe()
        canvas = self.driver.find_element_by_id('ngm-uicore2-root')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 350, 620).click().perform()  # '確定'
        for i in range(10):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        ActionChains(self.driver).move_by_offset(-150, 0).click().perform()  # '-'
        for j in range(20):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        ActionChains(self.driver).move_by_offset(800, 0).click().perform()  # '旋轉'
        time.sleep(6)
        for k in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(6)
        self.driver.close()
        self.switch_window()
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    '''卡在是否關掉聲音那關，用ActionChain沒有反應'''
    def goFBGelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        FBG_elgame = self.driver.find_element_by_css_selector('[ng-click="toJv8Html()"]')  # FBG发宝电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(FBG_elgame).perform()
        time.sleep(6)
        self.switch_window()
        self.switch_iframe()
        time.sleep(1)
        self.driver.find_element_by_css_selector('[title="松鼠战士"]').click()
        time.sleep(30)
        self.switch_window()
        self.switch_iframe()
        self.switch_iframe()
        self.switch_iframe()
        checkbox = self.driver.find_element_by_css_selector('.button--secondary')
        self.driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(3)
        canvas = self.driver.find_element_by_id('gcore-root')
        ActionChains(self.driver).move_to_element_with_offset(canvas, 385, 766).click().perform()  # '-'數
        for i in range(6):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        ActionChains(self.driver).move_by_offset(-190, 0).click().perform()
        for j in range(25):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(850, 0).click().perform()  # 轉動開始
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)
    '''
    彩票游戏
    樂透有可能閉盤，就算閉盤也會執行不會報錯。
    若閉盤就不會有注單
    '''
    # def goSYlottery(self):
    #     lobby_lottery = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[7]/a')  # "彩票游戏"下拉式選單
    #     sy_lottery = self.driver.find_element_by_css_selector('[ng-click="toSyLottery()"]')  # SY双赢彩票
    #     ActionChains(self.driver).move_to_element(lobby_lottery).click(sy_lottery).perform()
    #     time.sleep(8)
    #     self.switch_window()
    #     time.sleep(2)
    #     ActionChains(self.driver).move_by_offset(145, -58).click().perform() # 小
    #     time.sleep(0.5)
    #     ActionChains(self.driver).send_keys('5').perform()
    #     time.sleep(0.5)
    #     ActionChains(self.driver).send_keys(Keys.ENTER).perform()  # 確認
    #     time.sleep(0.5)
    #     ActionChains(self.driver).send_keys(Keys.ENTER).perform()  # 再確認
    #     time.sleep(8)
    #     self.driver.close()
    #     self.switch_window()
    #     time.sleep(3)
    #
    # '''体育赛事'''
    # def go3singsport(self):
    #     lobby_sport = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[6]/a')  # "体育赛事"下拉式選單
    #     _3sing_sport = self.driver.find_element_by_css_selector('[ng-click="toSingSport()"]')  # 三昇体育
    #     ActionChains(self.driver).move_to_element(lobby_sport).click(_3sing_sport).perform()
    #     time.sleep(5)
    #     self.switch_window()
    #     self.switch_iframe()
    #     multiple = self.driver.find_element_by_css_selector('[class="a_link_gamemanu a_link_gamemanu_sc8"]')
    #     self.driver.execute_script("arguments[0].click();", multiple)  # 混合过关
    #     time.sleep(3)
    #     ActionChains(self.driver).move_by_offset(-110, 40).click().perform()  # 明天
    #     time.sleep(1)
    #     ActionChains(self.driver).move_by_offset(230, 190).click().perform()  # 串關-大-1
    #     time.sleep(1)
    #     ActionChains(self.driver).send_keys('5').perform()
    #     time.sleep(1)
    #     ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    #     time.sleep(1)
    #     for j in range(4):
    #         ActionChains(self.driver).move_by_offset(0, 125).click().perform()  # 串關-大-2,3
    #         time.sleep(1)
    #         ActionChains(self.driver).send_keys('5').perform()
    #         time.sleep(1)
    #         ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    #         time.sleep(1)
    #     ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    #     time.sleep(3)
    #     ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    #     time.sleep(3)
    #     self.driver.close()
    #     self.switch_window()
    #     time.sleep(3)

    # def goSABAsport(self):
    #     lobby_sport = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[6]/a')  # "体育赛事"下拉式選單
    #     saba_sport = self.driver.find_element_by_css_selector('[ng-click="toSabaGame()"]')  # 沙巴体育
    #     ActionChains(self.driver).move_to_element(lobby_sport).click(saba_sport).perform()
    #     time.sleep(10)
    #     self.switch_window()
    #     ActionChains(self.driver).move_by_offset(-130, -100).click().perform()  # 串關
    #     time.sleep(4)
    #     ActionChains(self.driver).move_by_offset(30, 170).click().perform()  # 串關-1
    #     time.sleep(2)
    #     for j in range(4):
    #         ActionChains(self.driver).move_by_offset(0, 130).click().perform()  # 串關-大-2,3
    #         time.sleep(2)
    #     ActionChains(self.driver).send_keys('10').perform()
    #     time.sleep(1)
    #     ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    #     time.sleep(1)
    #     ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    #     time.sleep(8)
    #     self.driver.close()
    #     self.switch_window()
    #     time.sleep(3)
    #
    # def goCRsport(self):
    #     lobby_sport = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[6]/a')  # "体育赛事"下拉式選單
    #     cr_sport = self.driver.find_element_by_css_selector('[ng-click="toIboSport()"]')  # 皇冠体育
    #     ActionChains(self.driver).move_to_element(lobby_sport).click(cr_sport).perform()
    #     time.sleep(14)
    #     self.switch_window()
    #     ActionChains(self.driver).move_by_offset(-540, -75).click().perform()  # 综合过关
    #     time.sleep(4)
    #     ActionChains(self.driver).move_by_offset(80, -150).click().perform()  # 明日
    #     for i in range(3):
    #         time.sleep(2)
    #         ActionChains(self.driver).move_by_offset(300, 130).click().perform()  # 串關1
    #         for j in range(4):
    #             ActionChains(self.driver).move_by_offset(0, 90).click().perform()  # 串關2.3.4.5
    #             time.sleep(2)
    #         ActionChains(self.driver).send_keys('2').perform()
    #         time.sleep(1)
    #         ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    #         time.sleep(1)
    #         ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    #         time.sleep(5)
    #         ActionChains(self.driver).move_by_offset(-300, -490).click().perform()  # 在案一次明日
    #     self.driver.close()
    #     self.switch_window()
    #     time.sleep(3)
    #
