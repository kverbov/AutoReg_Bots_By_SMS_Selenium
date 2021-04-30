
# -*- coding: utf-8 -*-
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains

# from actions import Actions as acts
from selenium.webdriver.support.wait import WebDriverWait

from config import Config
from log import Log
import random


class Sms:#unittest.TestCase):
    confirmCodeWebElement=None
    phoneNumber='None'

    def __init__(self, url, login, password, proxyfile=None, useragent=None, cookies=None):
        self.login = login
        self.password = password
        self.url=url
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(r"--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data");
        chrome_options.add_argument(r"--profile-directory=Default");

        self.driver = webdriver.Chrome('chromedriver76.exe', chrome_options=chrome_options)
        self.driver = self.driver
        self.driver.implicitly_wait(Config.waittimeout)

        # driver.get(Config.curDir()+r'\HTML\index.htm')
        self.driver.get(url)
        time.sleep(Config.waittimeout)
        return

        if proxyfile!=None:
            chrome_options.add_extension(proxyfile)




        if useragent!=None:
            chrome_options.add_argument("--user-agent=" + useragent)
        # driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)


        driver.delete_all_cookies()

        if cookies != None:
            # Устанавливаем кукисы в браузере
            for cookie in cookies:
                # Удаляем параметр 'expiry',  который вызывает иключение в драйвере
                if'expiry' in cookie.keys():
                    cookie.pop('expiry')
                driver.add_cookie(cookie)
            driver.add_cookie({'name': 'HSID','value': 'AaR-3BkYwVWxgoDH0', 'path': '/', 'secure': False, 'domain': 'youtube.com', 'expiry': 1629133134, 'httpOnly': True})

    def __del__(self):
        if(self.driver!=None):
            Log.write('Деструктор - Уничтожения обхекта webdriver')
            self.driver.quit()

    def logIn(self):
        driver = self.driver
        # driver.get("https://youtube.com")
        # buttonList = driver.find_elements_by_id('button')

        # поиск кнопки ВОЙТИ
        menu = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/ul/li[2]/a')
        menu.click()
        enter = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/ul/li[2]/ul')
        enter.click()

        # Ввод логин/пароль
        email = driver.find_element_by_name('email')
        email.send_keys(self.login)
        password = driver.find_element_by_name('pass')
        password.send_keys(self.password)

        # Капча
        capcha=driver.find_element_by_xpath('/html/body/div[2]')
        ActionChains(driver).move_to_element(capcha).click(capcha).perform()

        # Проверяем что залогинились Успешно
        a = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/ul/li[1]/ul/li[1]/a')
        if str(a.get_attribute('href')).find('javascript:void(0)')>-1:
            Log.write('Логин успешный '+self.login + '\t' + self.password )
        else:
            Log.write('Логин НЕ успешный ' + self.login + '\t' + self.password)

    def getConfirmCode(self)->str:
        # Ожидаем когда высветится код
        driver=self.driver
        # driver.refresh()

        #         Ожидаем когда появить код подтверждения
        while True:
            # Определяем количество SMS заказов
            try:
                # items = WebDriverWait(driver, 30).until(
                #     EC.presence_of_all_elements_located((By.XPATH, '//*[@class="smsunit"]')))
                item=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[6]')
            except:
                Log.write('Не нашли элемент XPATH= //*[@class="smsunit"] ')
                return None

            if item.text=='Загрузка':
                time.sleep(random.randrange(30, 60))
                Log.write('Код пока не появился - ожидаем  '+self.phoneNumber)
            else:
                Log.write('Код появился  ' + self.phoneNumber+' | ' +item.text)
                return    item.text

        return None

    def buyNumber(self)->str:
        # Переход на главную
        # self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/a/img').click()
        self.driver.get(self.url)

        #  ставим радио кнопку Google
        menu = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/form/div[5]')
        list = menu.find_elements_by_xpath('//*[@class="service-item cell"]')
        for item in list:
            if item.get_attribute('service') == 'gl':
                count = item.find_element_by_class_name('price-label').find_elements_by_tag_name('span')[0].text
                index=count.find(' шт')
                n=count[0:index]
                if int(n)<1:
                    Log.write('Нет в наличии номеров  для покупки '+self.url)
                    sys.exit()
                    return None
                item.click()
                break

        #  Клик ПОЛУЧИТЬ НОМЕР
        button = self.driver.find_element_by_xpath('//*[@class="button main-left-button"]')
        button.click()
        time.sleep(5)

        # Берем номер телефона
        # Отслеживаем состояние таблицы
        try:
            table = self.driver.find_element_by_xpath('//table[@class="responsive"]').find_element_by_tag_name(
                'tbody')
        except Exception as e:
            Log.write(e)
            return None
        rows = table.find_elements_by_tag_name('tr')
        activeIndex = 0
        for tr in rows:
            if tr.find_elements_by_tag_name('td')[4].text.find('Ожидание') > -1:
                self.phoneNumber = tr.find_elements_by_tag_name('td')[3].text
                return self.phoneNumber 
            activeIndex += 1

        return None

    def waitConfirmCode(self)->str:
        # Ожидаем когда высветится код
        # Переходим в текущие активации
        driver=self.driver
        driver.refresh()
        try:
            menu = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/ul/li[1]/a')
            menu.click()
        except WebDriverException as e:
            Log.write(e)
            return None

        # Берем номер телефона
        # Отслеживаем состояние таблицы
        try:
            table = self.driver.find_element_by_xpath('//table[@class="responsive"]').find_element_by_tag_name(
                'tbody')
        except Exception as e:
            Log.write(e)
            return None
        rows = table.find_elements_by_tag_name('tr')
        activeIndex = 0
        for tr in rows:
            if tr.find_elements_by_tag_name('td')[4].text.find('Ожидание') > -1:
                phoneNumber = tr.find_elements_by_tag_name('td')[3].text
                self.status = tr.find_elements_by_tag_name('td')[4]
                self.confirmCodeWebElement=tr.find_elements_by_tag_name('td')[5]
                break
            activeIndex += 1

        while self.status.text.find('Ожидание')>-1:
            Log.write(' - Ждем когда появится код активации ' + str(Config.waitConfirmationCodeTimeout)+ ' сек')
            time.sleep(Config.waitConfirmationCodeTimeout)
            self.driver.refresh()
        return self.confirmCodeWebElement.text