import os

class Config (object):
    '''входные параметры'''
    useragentpath='user-agents.txt'
    phrase = 'Владимир Поведский'
    login = '[MASKED]'
    password = 'MASKED'
    waittimeout=15
    waitConfirmationCodeTimeout=30
    SMS ={
        "smska.net": ['kostyan777@mail.ru','Lin123da'],
        "sms-reg.com": ['pro_10', 'Lin123da']
    }

    @staticmethod
    def curDir():
        return os.getcwd()