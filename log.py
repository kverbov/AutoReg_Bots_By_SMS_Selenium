# -*- coding: utf-8 -*-
from datetime import datetime


class Log:#unittest.TestCase):

    # def __init__(self):
    #     self.driver = webdriver.Chrome("C:\\Users\\User\\Downloads\\chromedriver_win32\\chromedriver.exe")
    #     self.driver.set_page_load_timeout(10)

    @staticmethod
    def write( text):
        rez= str(datetime.now()) + ' | ' + text
        print(rez)

    def test(self):
        print('Hello World')
        a=Log()
        a.write('Это мой лог')
