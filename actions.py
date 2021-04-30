# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import os
import zipfile
from log import Log


class Actions:#unittest.TestCase):

    def __init__(self):
        """"""
        self.driver = webdriver.Chrome("C:\\Users\\User\\Downloads\\chromedriver_win32\\chromedriver76.exe")
        self.driver.set_page_load_timeout(10)

    def __init__(self, driver):
        self.driver=driver

    @staticmethod
    def randomLetter()->str:
        import random
        import string
        return random.choice(string.ascii_letters)

    @staticmethod
    def compressfiles(files: list, zippath: str):
        startpath=os.getcwd()
        myzip = zipfile.ZipFile(zippath, 'w')
        for file in files:
            os.chdir(os.path.dirname(file))
            Log.write('Добвление файла {0} \n в архив {1}\n'.format(file,zippath))
            myzip.write(os.path.basename(file))

        myzip.close()
        Log.write('Архив создан  успешно')
        os.chdir(startpath)

    @staticmethod
    def waitForDissappear( webelmnt: WebElement, counter:int=10 ):
        timer=0
        while webelmnt.is_displayed()>-1:
            if timer>=counter:
                Log.write('Ошибка Ожидания исчезновения элемента '+webelmnt)
                return False
            time.sleep(1)
            timer+=1
        return True

    def searchChannel(self, phrase):
        driver =  self.driver
        input=driver.find_element_by_id('search')
        input.send_keys(phrase)
        time.sleep(1)
        button = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
        button.click()

        list=driver.find_elements_by_tag_name('ytd-channel-renderer')
        for item in list:
            title=item.find_element_by_id('channel-title')
            if(title.text==phrase):
                item.click()

                # Кликаем вкладку ВИДЕО
                list=driver.find_elements_by_tag_name('paper-tab')
                for item in list:
                    if(str(item.text).lower().find('видео')!=-1):
                        item.click()
                        Log.write('Перешли в раздел Видео ')
                        break

                return True

        return False


    def setLikeByTitle(self, titleText=''):
        driver =  self.driver
        driver.maximize_window()
        titleText=titleText.lower()
        # Ищем нужный ролик
        titles=driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[2]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer') #ytd-grid-video-renderer')
        found=False
        for title in titles:
            item=title.find_element_by_id('video-title')
            text=str(item.get_attribute('title')).lower()
            if(text.find(titleText)!=-1):
                Log.write('Нашли ролик по title - переходим на него')
                item.click()
                found=True
                break
        if(found==False):
            return False

        '''Кликаем  ЛАЙК'''
        list=driver.find_elements_by_tag_name('ytd-toggle-button-renderer')
        for item in list:
            if (item.find_element_by_id('button')):
                if( item.find_element_by_tag_name('yt-icon-button').get_attribute('aria-pressed')=='false'):
                    item.click()
                    Log.write('Поставили Лайк')
                    break
                else:
                    Log.write('Лайк уже установлен, проходим мимо')

    @staticmethod
    def CheckAccounts( filename, useragents):
        file = open(filename)
        accounts = {}
        for line in file:
            mas = line.replace('\n', '').replace(' ', '').replace('\t', '').strip().rsplit(';')
            accounts.update({mas[0]: mas[1]})

        i=0
        for key, value in accounts.items():
            lin = Login(key, value, useragents[i])
            if(lin.logIn() is True):
                Log.write('Логин успешный '+key+'\t'+value)
            else:
                Log.write('Логин НЕ успешный ' + key + '\t' + value)
            lin.driver.quit()
            if(i==len(accounts)-1):
                i=0
            else:
                i+=1

    def comment(self, url):
        pass

    def setLikeByUrl(self, url='NONE'):
        driver = self.driver
        driver.get(url)
        list = driver.find_elements_by_tag_name('ytd-toggle-button-renderer')
        for item in list:
            if (item.find_element_by_id('button')):
                if (item.find_element_by_tag_name('yt-icon-button').get_attribute('aria-pressed') == 'false'):
                    item.click()
                    Log.write('Поставили Лайк по ссылке ',url)
                    break
                else:
                    Log.write('Лайк уже установлен, проходим мимо')

    def setUseragent(self, agent):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", agent)
        self.driver = webdriver.Firefox(profile)


    # def setDislike(self):
    #     driver = self.driver
    #      list = driver.find_elements_by_tag_name('ytd-toggle-button-renderer')
    #     for item in list:
    #         if (item.find_element_by_id('button')):
    #             item.click()
    #             Log.write('Поставили Лайк')
    #
    #     input.send_keys(phrase)
    #     time.sleep(1)
    #     button = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
    #     button.click()
    #
    #     list=driver.find_elements_by_tag_name('ytd-channel-renderer')
    #
    #         title=item.find_element_by_id('channel-title')
    #         if(title.text==phrase):
    #             item.click()
    #             return True
    #
    #     return False