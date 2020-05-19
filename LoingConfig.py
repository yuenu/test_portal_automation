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
    driver.get('http://www.fnjtd.com/')

    def __init__(self):
        self.account = 'yuenu002'
        self.password = 'a123456'
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


class GameHall(PortalLoginConfig):
    """捕鱼游戏"""
    def goAPfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        AP_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[3]/li[5]')  # AP金蟾捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(AP_fish).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform() # 點擊0.1元炮場
        time.sleep(4)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.5)
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goFGbird(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        FG_bird = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[2]/li[4]')  # FG捕鸟达人
        ActionChains(self.driver).move_to_element(lobby_fish).click(FG_bird).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform() # 點擊"0.1倍場"
        time.sleep(4)
        for j in range(5):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.8)
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goFGfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        FG_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[1]/li[4]')  # FG美人捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(FG_fish).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform() # 點擊"0.1倍場"
        time.sleep(4)
        ActionChains(self.driver).move_by_offset(850, -190).click().perform()  # Close "x"
        for j in range(5):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.8)
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goGPKfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        GPK_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[2]/li[1]')  # GPK王者捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(GPK_fish).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(200, 150).click().perform()  # 點擊0.1元炮場
        time.sleep(4)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.5)
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goJDBfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        JDB_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[3]/li[8]')  # JDB龙王捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(JDB_fish).perform()
        time.sleep(14)
        self.switch_window()
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 點擊0.1元炮場
        time.sleep(4)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.5)
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(5)

    # TH捕魚關閉的話不會馬上把錢轉出來，後面有皆其他娛樂城的話不會帶錢進去
    def goTHfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        TH_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[3]/li[7]')  # TH李逵劈鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(TH_fish).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform() # 點擊0.1元炮場
        time.sleep(5)
        for j in range(70):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.2)
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(8)

    def goLEGfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        LEG_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[2]/li[9]')  # LEG捕鱼大作战
        ActionChains(self.driver).move_to_element(lobby_fish).click(LEG_fish).perform()
        time.sleep(10)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 點擊0.1元炮場
        time.sleep(5)
        ActionChains(self.driver).move_by_offset(880, 230).click().perform()  # 自動射擊
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(5)

    def goMTfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        MT_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[4]/li[9]')  # MT美天李逵劈鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(MT_fish).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(-300, 0).click().perform()  # 點擊0.1元炮場
        time.sleep(10)
        ActionChains(self.driver).move_by_offset(800, -240).click().perform()  # 點"x"
        for j in range(5):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.5)
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goMWfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        MW_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[1]/li[10]')  # MW千炮捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(MW_fish).perform()
        time.sleep(16)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 點擊0.1元炮場
        time.sleep(16)
        ActionChains(self.driver).move_by_offset(460, 5).click().perform()  # 點"確定"
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
        VG_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[2]/li[10]')  # VG龙王捕鱼
        ActionChains(self.driver).move_to_element(lobby_fish).click(VG_fish).perform()
        time.sleep(12)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform() # 點擊0.1元炮場
        time.sleep(7)
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 發炮
            time.sleep(0.5)
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goBSPfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        BSP_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[4]/li[11]')  # BSP千炮捕鱼王3D
        ActionChains(self.driver).move_to_element(lobby_fish).click(BSP_fish).perform()
        time.sleep(10)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(490, -280).click().perform()  # 點擊"x"
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(-780, 220).click().perform()  # 點擊0.1元炮場
        time.sleep(10)
        ActionChains(self.driver).move_by_offset(250, 415).click().perform()  # 點擊自動
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(5)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goYGfish(self):
        lobby_fish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a')  # "捕鱼游戏"下拉式選單
        goYGfish = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/div/ol[3]/li[12]')  # YG超级海王
        ActionChains(self.driver).move_to_element(lobby_fish).click(goYGfish).perform()
        time.sleep(10)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()  # 點擊0.1元炮場
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(115, 225).click().perform()  # 點擊自動
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(0, 0).click().perform()
        time.sleep(8)
        self.driver.close()
        self.switch_window()
        time.sleep(3)



    '''电子游艺'''
    def goAEelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        AEelgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/div/ol[1]/li[6]')  # AE阿米巴电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(AEelgame).perform()
        time.sleep(5)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(380, 520).click().perform()  # 案"一路發"
        self.switch_window()
        time.sleep(6)
        ActionChains(self.driver).move_by_offset(-160, -180).click().perform()
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(3)
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goPGelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        PGelgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/div/ol[4]/li[1]')  # PG电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(PGelgame).perform()
        time.sleep(5)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(-600, 250).click().perform()  # 案"双囍临门"
        self.switch_window()
        time.sleep(8)
        ActionChains(self.driver).move_by_offset(300, 300).click().perform() # "開始"
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(0, 80).click().perform()  # "減碼按鈕"
        for j in range(10):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(0.5)
        ActionChains(self.driver).move_by_offset(100, 0).click().perform()  # "轉動按鈕"
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(4)
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goSWelgame(self):
        lobby_elgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/a')  # "电子游艺"下拉式選單
        SWelgame = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[5]/div/ol[1]/li[5]')  # 天风电子游艺
        ActionChains(self.driver).move_to_element(lobby_elgame).click(SWelgame).perform()
        time.sleep(5)
        self.switch_window()
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(350, 150).click().perform()  # 案"天上凤凰"
        self.switch_window()
        time.sleep(12)
        ActionChains(self.driver).move_by_offset(-200, 220).click().perform() # "開始"
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(-280, 70).click().perform()  # "減碼按鈕"
        for j in range(10):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(0.5)
        ActionChains(self.driver).move_by_offset(800, 0).click().perform()  # "轉動按鈕"
        for j in range(3):
            ActionChains(self.driver).move_by_offset(0, 0).click().perform()
            time.sleep(4)
        time.sleep(10)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    '''
    彩票游戏
    樂透有可能閉盤，就算閉盤也會執行不會報錯。
    若閉盤就不會有注單
    '''
    def goSYlottery(self):
        lobby_lottery = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[7]/a')  # "彩票游戏"下拉式選單
        SY_lotery = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[7]/ol/li[8]')  # SY双赢彩票
        ActionChains(self.driver).move_to_element(lobby_lottery).click(SY_lotery).perform()
        time.sleep(8)
        self.switch_window()
        time.sleep(2)
        ActionChains(self.driver).move_by_offset(145, -58).click().perform() # 小
        time.sleep(0.5)
        ActionChains(self.driver).send_keys('5').perform()
        time.sleep(0.5)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()  # 確認
        time.sleep(0.5)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()  # 再確認
        time.sleep(8)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    '''体育赛事'''
    def go3singSport(self):
        lobby_sport = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[6]/a')  # "体育赛事"下拉式選單
        _3sing_sport = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[6]/ol/li[1]')  # 三昇体育
        ActionChains(self.driver).move_to_element(lobby_sport).click(_3sing_sport).perform()
        time.sleep(5)
        self.switch_window()
        ActionChains(self.driver).move_by_offset(-280, -20).click().perform()  # 混合过关
        time.sleep(3)
        ActionChains(self.driver).move_by_offset(-110, 40).click().perform()  # 明天
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(230, 190).click().perform()  # 串關-大-1
        time.sleep(1)
        ActionChains(self.driver).send_keys('5').perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        for j in range(4):
            ActionChains(self.driver).move_by_offset(0, 125).click().perform()  # 串關-大-2,3
            time.sleep(1)
            ActionChains(self.driver).send_keys('5').perform()
            time.sleep(1)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(8)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goSABASport(self):
        lobby_sport = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[6]/a')  # "体育赛事"下拉式選單
        SABA_sport = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[6]/ol/li[2]')  # 沙巴体育
        ActionChains(self.driver).move_to_element(lobby_sport).click(SABA_sport).perform()
        time.sleep(10)
        self.switch_window()
        ActionChains(self.driver).move_by_offset(-130, -100).click().perform()  # 串關
        time.sleep(4)
        ActionChains(self.driver).move_by_offset(30, 170).click().perform()  # 串關-1
        time.sleep(2)
        for j in range(4):
            ActionChains(self.driver).move_by_offset(0, 130).click().perform()  # 串關-大-2,3
            time.sleep(2)
        ActionChains(self.driver).send_keys('10').perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(8)
        self.driver.close()
        self.switch_window()
        time.sleep(3)

    def goCRSport(self):
        lobby_sport = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[6]/a')  # "体育赛事"下拉式選單
        CR_sport = self.driver.find_element_by_xpath('//*[@id="nav"]/ul/li[6]/ol/li[7]')  # 皇冠体育
        ActionChains(self.driver).move_to_element(lobby_sport).click(CR_sport).perform()
        time.sleep(10)
        self.switch_window()
        ActionChains(self.driver).move_by_offset(-540, -85).click().perform()  # 综合过关
        time.sleep(4)
        ActionChains(self.driver).move_by_offset(80, -140).click().perform()  # 明日
        for i in range(3):
            time.sleep(2)
            ActionChains(self.driver).move_by_offset(300, 130).click().perform()  # 串關1
            for j in range(4):
                ActionChains(self.driver).move_by_offset(0, 90).click().perform()  # 串關2.3.4.5
                time.sleep(2)
            ActionChains(self.driver).send_keys('2').perform()
            time.sleep(1)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(5)
            ActionChains(self.driver).move_by_offset(-300, -490).click().perform()  # 在案一次明日
        self.driver.close()
        self.switch_window()
        time.sleep(3)

