# -*- coding: utf-8 -*-
import sys
import time
import random
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from config import Config
from log import Log
from selenium.webdriver.support import expected_conditions as EC

class Sms:#unittest.TestCase):
    confirmCodeWebElement=None
    phoneNumber=None

    def __repr__(self):
        return "SMS({login}, {password}, {driver})".format(login=self.confirmCodeWebElement, password=self.phoneNumber, driver=self.driver)

    def __init__(self, login, password, proxyfile=None, useragent=None, cookies=None):
        self.login = login
        self.password = password
        self.url=r'https://sms-reg.com/ui.php?action=getsms'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(r"--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data");
        chrome_options.add_argument(r"--profile-directory=Default");

        self.driver = webdriver.Chrome('chromedriver76.exe', chrome_options=chrome_options)
        self.driver.implicitly_wait(Config.waittimeout)

        # driver.get(Config.curDir()+r'\HTML\index.htm')
        self.driver.get(self.url)
        time.sleep(Config.waittimeout)
        return

        if proxyfile!=None:
            chrome_options.add_extension(proxyfile)

        if useragent!=None:
            chrome_options.add_argument("--user-agent=" + useragent)
        # driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)


        driver.delete_all_cookies()

        # if cookies != None:
        #     # Устанавливаем кукисы в браузере
        #     for cookie in cookies:
        #         # Удаляем параметр 'expiry',  который вызывает иключение в драйвере
        #         if'expiry' in cookie.keys():
        #             cookie.pop('expiry')
        #         driver.add_cookie(cookie)
        #     driver.add_cookie({'name': 'HSID','value': 'AaR-3BkYwVWxgoDH0', 'path': '/', 'secure': False, 'domain': 'youtube.com', 'expiry': 1629133134, 'httpOnly': True})

    def __del__(self):
        if(self.driver!=None):
            Log.write('Деструктор - Уничтожения обхекта webdriver')
            self.driver.quit()

    def cancel(self)->bool:
        driver=self.driver
        driver.get('https://sms-reg.com/ui.php?action=getsms')
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        
        # cancelButton = self.driver.find_element_by_xpath('//*[@id="stream"]/div/span[2]/button')
        # Определяем количество SMS заказов
        while True:
            try:
                items = WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@class="smsunit"]')))

                mas = []
                for item in items:
                    mas.append(item.text)
                lastindex = len(mas) - 1
                break
            except:
                Log.write('Не нашли элемент XPATH= //*[@class="smsunit"] ')
                return False

        # Клик кнопка ИСпользован
        try:
            items = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="smsunit"][{0}]'.format(lastindex + 1))))
            Log.write('Нашли кнопку ИСОЛЬЗОВАН')
            used = items.find_element_by_xpath('//*[@class="used"]')
            Log.write('Клик  кнопку ИСПОЛЬЗОВАН ' + self.phoneNumber)
            used.click()
        except:
            Log.write('Не дождались кнопки ИСПОЛЬЗОАВН')
            return False

        return True

    def buyNumber(self)->bool:
        # Переход на главную
        # self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/a/img').click()
        self.driver.get(self.url)
        driver = self.driver

        # Покупаем номер
        menu = driver.find_element_by_xpath('//*[@id="s1"]')
        menu.click()
        time.sleep(2)
        Russia=driver.find_element_by_xpath('//*[@id="label_ru"]')
        Russia.click()

        service = driver.find_element_by_xpath('//*[@id="s2"]')
        service.click()
        Google=driver.find_element_by_xpath('//*[@id="opt1"]')
        Google.click()
        time.sleep(2)

        submit=driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div[1]/span[3]')
        submit.click()
        time.sleep(15)

        # Определяем количество SMS заказов
        while True:
            try:
                items = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="smsunit"]')))
            except:
                Log.write('Не нашли элемент XPATH= //*[@class="smsunit"] ')
                return False
            mas=[]
            for item in items:
                mas.append(item.text)
            lastindex=len(mas)-1
            text=mas[lastindex].splitlines()
            if text[1].find('подготовка номера')>-1:
                time.sleep(random.randrange(7, 15 ,1))
                # driver.refresh()
                continue
            else:
                self.phoneNumber = text[0]
                break

        # Клик кнопка ГОТОВО
        try:
            item = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@class="smsunit"][{0}]'.format(lastindex+1))))
            ready = item.find_element_by_tag_name('button')
            ready.click()
        except:
            Log.write('Не дождались кнопки ГОТОВО')
            return False

        return True


    def getConfirmCode(self)->str:
        # Ожидаем когда высветится код
        driver=self.driver
        # driver.refresh()

        #         Ожидаем когда появить код подтверждения
        while True:
            # Определяем количество SMS заказов
            try:
                items = WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@class="smsunit"]')))
            except:
                Log.write('Не нашли элемент XPATH= //*[@class="smsunit"] ')
                return None
            mas = []
            for item in items:
                mas.append(item.text)
            lastindex = len(mas) - 1
            text = mas[lastindex].splitlines()
            if self.phoneNumber != text[0]:
                Log.write('Код не пришел , номер уплыл  '+self.phoneNumber)
                sys.exit()

            if text[2].find('ожидаем')>-1:
                Log.write('Ожидаем код ')
                time.sleep(random.randrange(15,30))
                continue
            else:
                return text[2].replace('G-','')
        return None

    def logIn(self):
        driver = self.driver

        # Ввод логин/пароль
        email = driver.find_element_by_name('email')
        email.send_keys(self.login)
        password = driver.find_element_by_name('pass')
        password.send_keys(self.password)

        # Капча
        capcha = driver.find_element_by_xpath('/html/body/div[2]')
        ActionChains(driver).move_to_element(capcha).click(capcha).perform()

        # Проверяем что залогинились Успешно
        a = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/ul/li[1]/ul/li[1]/a')
        if str(a.get_attribute('href')).find('javascript:void(0)') > -1:
            Log.write('Логин успешный ' + self.login + '\t' + self.password)
        else:
            Log.write('Логин НЕ успешный ' + self.login + '\t' + self.password)
