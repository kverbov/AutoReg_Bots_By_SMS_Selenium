# -*- coding: utf-8 -*-
#from selenium import webdriver
from config import Config
from login import Login
from sms.sms_reg.sms import Sms
# from sms.smska.sms import Sms

'''   Читаем список Аккаунтов и их параметров      '''
# f=open(Config.curDir()+'\Кука [MASKED] Заход с работы.txt','r')
# text=f.readlines()
# cookies=[]
# for item in text:
#     cookies.append(eval(item))
login=Login(Config.login, Config.password)
            # r".\proxy\92.63.102.34.zip",
            # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            # cookies)


# покупаем номер                            
# s=Sms("https://smska.net", Config.SMS.get('smska.net')[0],Config.SMS.get('smska.net')[1])
# success=s.buyNumber()
# if success==False:
#      s.driver.quit()
#      exit()

# Создаем акаунт Google и ждем номер
login.createAccount('Инна ', 'Микранова', 'imikranova2019', 'Lin123da',s.phoneNumber,s)
exit()

'''Поиск канала'''
# driver= webdriver.Chrome("C:\\Users\\User\\Downloads\\chromedriver_win32\\chromedriver.exe")
# driver.implicitly_wait(10)
# driver.get("https://youtube.com")
# time.sleep(1)
# nav=Actions(driver)
# if(nav.searchChannel(phrase)):
#     print('Нашли канал '+'"'+phrase+'"')
# else:
#     print('Не нашли канал ' + '"' + phrase + '"')

#nav.setLikeByTitle('Какой язык программирования выбрать новичку для фриланса и работы за рубежом - Python, Java, C#')
# likeUrl='https://www.youtube.com/watch?v=tYLDxU7WR98'
# nav.setLikeByUrl(likeUrl)
# driver.quit()
