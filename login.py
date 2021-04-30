# -*- coding: utf-8 -*-
import sys
import os
import time
from actions import Actions
from selenium.webdriver import ActionChains
import random
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from config import Config
from log import Log as l
from sms.smska.sms import Sms
from selenium.webdriver.support import expected_conditions as EC
import glob

class Login:#unittest.TestCase):

    def __init__(self, login, password, proxyfile=None, useragent=None, cookies:list=None):
        self.basepath=os.getcwd()
        self.login = login
        self.password = password
        chrome_options = webdriver.ChromeOptions()

        if proxyfile!=None:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_extension(proxyfile)
        else:
            chrome_options.add_extension(self.get_proxyext(self.basepath+r'\Proxy',random.randrange(1,70,1)))

        if useragent!=None:
            chrome_options.add_argument("--user-agent=" + useragent)
        else:
            chrome_options.add_argument("--user-agent=" + self.get_useragent(os.getcwd() + r"\\" + Config.useragentpath))

        self.driver = webdriver.Chrome('chromedriver76.exe', chrome_options=chrome_options)
        driver=self.driver
        driver.implicitly_wait(Config.waittimeout)


        # Без перехода на сайта невозможно установить Cookie
        driver.get('https://mail.ru')
        driver.maximize_window()
        time.sleep(10)
        driver.delete_all_cookies()

        # Устанавливаем кукисы в браузере
        if cookies != None:
            for cookie in cookies:
                val = cookie.get('expiry', None)
                if val == None:
                    continue
                cookie['expiry'] = int(cookie['expiry'])
                driver.add_cookie(cookie)
                l.write(r'Установили КУКИ для ютуба:\n Логин: '+self.__repr__()+'\n'+str(cookie))
            
    def __del__(self):
        if(self.driver!=None):
            l.write('Деструктор Login - Уничтожения обхекта webdriver')
            self.driver.quit()

    #def __str__(self):
     #   return 'class Login: conatins attribute login= '+self.login

    def __repr__(self):
        return "Login({login}, {password}, {driver})".format(login=self.login, password=self.password, driver=self.driver)


    def logIn(self):
        driver = self.driver
        driver.get("https://youtube.com")
        buttonList = driver.find_elements_by_id('button')

        #   Кликаем Войти
        for button in buttonList:
            if (button.text.lower().find("войти") != -1):
                print("Found \r\n", button.text, "\r\n _______________________")
                try:
                    button.click()
                    WebDriverWait(driver, 3)
                except Exception:
                    return False

                #   Ввод логина
                driver.find_element_by_xpath('//*[@id="identifierId" and @type="email"]').send_keys(self.login)
                driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/span/span').click()
                time.sleep(1)

                # Ввод пароля
                driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(self.password)
                button=driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/span/span')
                while not button.is_displayed():
                    time.sleep(1)

                button.click()
                time.sleep(2)

                #   если кнопка "Далее" не исчезла , значит пароль неверный
                try:
                    if(button.is_displayed()>-1):
                        return False
                except WebDriverException as e:
                    pass
                    #l.write(str(e))

                #   надпись "Не удалось войти в аккаунт" - Браузер не поддерживается
                try:
                    item = driver.find_element_by_xpath('//*[@id="headingText" ]/span[contains(text(),"Не удалось войти в аккаун")]')
                    a = str(item.text)
                    if (item.is_displayed() and a.find('Не удалось войти в аккаун') > -1):
                        item=driver.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/span/div/div[1]')
                        l.write('Ошибка - Логин/Пароль: '+self.login+'\t'+ self.password+ '\t - '+ item.text)
                        return False
                except Exception as e:
                    return True

                #   надпись "Подтвердите, что это именно вы"
                try:
                    item = driver.find_element_by_xpath('//*[@id="headingText" ]/span[contains(text(),"Подтвердите, что")]')
                    a = str(item.text)
                    if (item.is_displayed() and a.find('Не удалось войти в аккаун') > -1):
                        item=driver.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/span/div/div[1]')
                        l.write('Ошибка - Логин/Пароль: '+self.login+'\t'+ self.password+ '\t - '+ item.text)
                        return False
                except Exception as e:
                    l.write(str(e))
                    return False



                #   Надпись  "Подтвердите " появилась?
                try:
                    item=driver.find_element_by_xpath('//*[@id="headingText" ]/span[contains(text(),"Подтвердите")]')
                    a = str(item.text)
                    if (item.is_displayed() and a.find('Подтвердите')>0):
                        l.write('Ошибка - ',a)
                        break
                except Exception as e:
                    l.write(str(e))
                    return False
                l.write('Валидны. Логин Успешен ' + self.login + '\t' + self.password)
                return True

        return False

    def sendPhoneNumber(self,phonenumber):
        # Вводим номер телефона
        telinput = self.driver.find_element_by_xpath('//*[@id="phoneNumberId"]')
        telinput.clear()
        telinput.send_keys('+'+phonenumber)

        # Климк  кнопка "Далее"
        submit = self.driver.find_element_by_xpath('//*[@id="gradsIdvPhoneNext"]/span')
        try:
            submit.click()
            time.sleep(2)
        except WebDriverException as e:
            print('Нажимаем кнопку Далее - Ошибка ' + e.msg)

    def get_proxyext(self, proxyex_dir, index:int)->str:
        ''' index: int  - индекс в человеческом формате, поэтому отнимаем единичку'''
        dir= glob.glob(proxyex_dir+"\*.zip")
        l.write('Запрошен прокси '+dir[index-1])
        return dir[index]

    def get_useragent(self, path)->str:
        index=random.randrange(1,35,1)
        with open(path,'r') as file:
            for i in range(0,index):
                file.readline()
            return file.readline()

    def createAccount(self, name,surname, username, password,phonenumber, sms)->bool:
        if phonenumber==None:
            l.write('Номера телефона нет  - ВЫХОД')
            sys.exit()
        driver = self.driver
        # driver.get(Config.curDir()+r"\index.htm")
        driver.get('https://youtube.com')

        # button = driver.find_elements_by_xpath(r'//*[@id="guide-builder-promo-buttons"]/a/span')

        # button = driver.find_elements_by_xpath('// *[ @ id = "buttons"] / ytd - button - renderer / a')
        #
        # #   Кликаем Войти
        # if (button.text.lower().find("войти") != -1):
        #     print("Found \r\n", button.text, "\r\n _______________________")
        #     try:
        #         button.click()
        #         WebDriverWait(driver, 3)
        #     except Exception:
        #         return False
        # else:
        #     l.write('Не найден кнопка "ВОЙТИ"')
        #     return False

        # Нажать Создать аккаунт

        buttonList = driver.find_elements_by_id('button')

        #   Кликаем Войти
        for button in buttonList:
            if (button.text.lower().find("войти") != -1):
                print("Found \r\n", button.text, "\r\n _______________________")
                try:
                    button.click()
                    WebDriverWait(driver, 3)
                    break
                except Exception:
                    return False

        # container = driver.find_elements_by_xpath(r'//*[@id="view_container"]/div/div/div[2]/div/div[2]')
        button=driver.find_element_by_xpath('html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div/span/span')
        button.click()
        time.sleep(2)

        # Жмем ДЛЯ СЕБЯ
        item=driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[3]/div/div/span[1]/div[2]/div')
        item.click()
        time.sleep(2)

        # проверяем заголовок
        header = driver.find_element_by_xpath(r'//*[@id="headingText"]')
        WebDriverWait(driver,30)
        if header.text.lower().find('создайте аккаунт google') == -1:
            # l.write('Создание аккаунта / Ошибка - Не нашли надпись "Создайте аккаунт Google" ')
            print('Создание аккаунта / Ошибка - Не нашли надпись "Создайте аккаунт Google" ')
            return False

        # Выбираем создание Google аккаунта
        googleAcc = driver.find_element_by_xpath('//*[@id="view_container"]/form/div[2]/div/div[1]/div[2]/button')
        googleAcc.click()

        # Заполняем поля
        inputs = driver.find_elements_by_tag_name('input')
        inputs[0].send_keys(name)
        time.sleep(random.randrange(2,10))
        inputs[1].send_keys(surname)
        time.sleep(random.randrange(10, 20))

        # Выбираем предложенный вариант логина от Гугла
        index = random.randrange(1, 3, 1)
        inputData=inputs[2].get_attribute('data-initial-value')
        l.write('Предложен логин - '+inputData)
        choice=random.randrange(0,1)
        if choice>0:
                inputs[2].clear()
                inputs[2].send_keys(username)
                time.sleep(random.randrange(2, 10))
                l.write('Вели свой логин '+username)
        else:
            if inputData == '':
                choice = random.randrange(0, 1)
                if choice>0:
                    try:
                        loginList = driver.find_element_by_xpath('//*[@id="usernameList"]').find_elements_by_tag_name(
                            'li')
                        item = loginList[index]
                        item.click()
                        l.write('Выбран логин из вариантов предложенных  Google - ' + username)
                    except:
                        inputs[2].clear()
                        inputs[2].send_keys(username)
                        time.sleep(random.randrange(2, 10))
                        l.write('Не найден список предложенных логинов Google. Вбиваем свой вариант. - ' + username)
                else:
                    inputs[2].clear()
                    inputs[2].send_keys(username)
                    time.sleep(random.randrange(2, 10))
                    l.write('Вели свой логин ' + username)
            else:
                l.write('Автозаполнение Google непустое, оставляем как есть - '+inputData)

        time.sleep(random.randrange(2,10))
        inputs[3].send_keys(password)
        time.sleep(random.randrange(2,10))
        inputs[4].send_keys(password)

        # Клик ДАЛЕЕ
        nextButton=driver.find_element_by_xpath('//*[@id="accountDetailsNext"]/span/span')
        nextButton.click()

        # Проверяем что логин не занят
        while True:
            try:
                message = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="view_container"]/form/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div')))
                l.write(r'Логин не прошел регистрацию:\n'+message.text)
                inputs[2].send_keys(Actions.randomLetter())
                time.sleep(random.randrange(2, 10))
                nextButton.click()
            except WebDriverException as e:
                l.write('Логин прошел регистрацию , идем дальше '+self.login)
                break

        # проверяем надпись что логин не может быть зарегистрирован
        try:
            message =message = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="view_container"]/form/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div')))
            l.write(r'Логин не прошел регистрацию:\n'+message.text)
            sys.exit()
        except WebDriverException as e:
            l.write('Логин прошел регистрацию , идем дальше ')

        # Ждем когда исчезнет форма заполнения
        while len(inputs)>1:
            time.sleep(1)
            l.write('Этап - Ждем когда исчезнет форма заполнения  ')
            inputs = driver.find_elements_by_tag_name('input')

        # Заполняем номер телефона и выбираем РЕГИОН
        # driver.find_element_by_xpath('//*[@id="countryList"]/div[1]/div[1]/div[1]').click()
        # countries = self.driver.find_element_by_xpath(r'//*[@id="countryList"]/div[2]/*/span')
        # ActionChains.send_keys(Keys.PAGE_DOWN).perform()
        # ActionChains.send_keys(Keys.PAGE_DOWN).perform()
        # ActionChains.send_keys(Keys.PAGE_DOWN).perform()
        # drp = Select(country)
        # drp.select_by_index(random.randrange(1, 12, 1))

        self.sendPhoneNumber(phonenumber)

        # Проверяем сообщение - ЭТОТ НОМЕ НЕ МОЖЕТ БЫТЬ ИСПОЛЬЗОВАН
        cnt=random.randrange(2,5)
        i=0
        while True:
            try:
                message = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="view_container"]/form/div[2]/div/div[1]/div/div[2]/div[2]/div[2]')))
                messagetext=message.text
            except:
                l.write('Сообщения нет, значит номер прошел')
                break

            if str(messagetext).find('Этот номер нельзя ') > -1:
                l.write(message.text)
                sms.cancel()
                if sms.buyNumber()==False:
                    l.write('Не получилось купить номер '+sms)
                    sys.exit()

                phonenumber = sms.phoneNumber
                self.sendPhoneNumber(phonenumber)
                if i==cnt:
                    l.write('Попыток подбора номера: '+cnt + 'Выход.')
                    sys.exit()
                i+=1
            else:
                break

        # Ждем код подтверждения и вводим
        code=sms.getConfirmCode()
        confirm = driver.find_element_by_xpath('//*[@id="code"][@name="code"]')
        l.write('Вводим код подтверждения '+code)
        confirm.send_keys(code)
        l.write('Клик ПОДТВЕРДИТЬ ')
        button=driver.find_element_by_xpath('//*[@id="gradsIdvVerifyNext"]/span/span')
        button.click()
        time.sleep(random.randrange(2,10))

        # Путь к надписи Подтверждение не отправлено
        # Произошла ошибка. Повторите попытку.
        '//*[@id="headingText"]/span'

        # ____________________________________________________________________________________________________________________________
        #   надпись "Не удалось войти в аккаунт" - Браузер не поддерживается
        try:
            item = driver.find_element_by_xpath(
                '//*[@id="headingText" ]/span[contains(text(),"Не удалось войти в аккаун")]')
            a = str(item.text)
            if (item.is_displayed() and a.find('Не удалось войти в аккаун') > -1):
                item = driver.find_element_by_xpath(
                    '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/span/div/div[1]')
                l.write('Ошибка - Логин/Пароль: ' + self.login + '\t' + self.password + '\t - ' + item.text)
                return False
        except Exception as e:
            l.write('Регистрация номера успешна.  Завершаем регистрацю, заполняем доп информацию.')
        time.sleep(random.randrange(2,10))

        # Заполняем оставшиеся поля

        day=self.driver.find_element_by_xpath(r'//*[@id = "day"]').send_keys(str(random.randrange(1, 29 ,1)))
        month=self.driver.find_element_by_xpath(r'//*[@id="month"]')
        drp = Select(month)
        drp.select_by_index(random.randrange(1, 12 ,1))
        year=self.driver.find_element_by_xpath(r'//*[@id="year"]').send_keys(str(random.randrange(1975, 2000,1)))
        gender=self.driver.find_element_by_xpath(r'//*[@id="gender"]')

        drp=Select(gender)
        drp.select_by_index(random.randrange(1,3,1))
        l.write('Доп поля заполнили')

        # Клик ДАЛЕЕ
        nextButton = driver.find_element_by_xpath(r'//*[@id="personalDetailsNext"]/span/span')
        nextButton.click()
        time.sleep(random.randrange(2,10))
        skipbutton=driver.find_element_by_xpath(r'//*[@id="view_container"]/form/div[2]/div/div[2]/div[1]/div[2]/button')
        skipbutton.click()
        time.sleep(random.randrange(2,10))

        # Принимаем соглашение

        acceptText=driver.find_element_by_xpath('//*[@id="view_container"]/form/div[2]/div/div/div/div[1]/span/div/div[1]')
        ActionChains(driver).move_to_element(acceptText).click(acceptText).perform()
        time.sleep(random.randrange(2,10))
        for i in range(0,random.randrange(4,10)):
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(3)
        acceptButton=driver.find_element_by_xpath('//*[@id="termsofserviceNext"]/span/span').click()

        # Сохраняем куки
        cookies=driver.get_cookies()
        f=open(os.getcwd()+r'\cookies.txt','a')
        f.write(username+r'\n')
        cookies = driver.get_cookies()
        f = open(os.getcwd() + r'\cookies.txt', 'a')
        f.writelines(str(cookies))
        f.close()
        return True