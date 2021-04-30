# -*- coding: utf-8 -*-
import os
import zipfile
from actions import Actions
from shutil import copyfile
from log import Log as l
from config import Config

manifest_src  = os.getcwd() + r'\Proxy\manifest.json'
background_src=os.getcwd() + r'\Proxy\background.js'

def generate(proxy_file, result_dir)->bool:
    copyfile(manifest_src, result_dir + r'\manifest.json')

    # f=open(os.getcwd()+r'\proxy.txt','r')
    i=0
    with open(proxy_file) as proxyf:
        for proxy in proxyf:
            i += 1
            print('-------------'+proxy + '------------')
            # Генерим ZIP архив для текущего прокси
            # proxy = proxyf.readline()
            ip =  proxy[proxy.find('@') + 1:proxy.find(':443')]
            with open(os.getcwd() + r'\Proxy\background.js', 'r') as background, open(os.getcwd() + r'\Proxy\rez.js',
                                                                                      'a') as  rez:
                for line in background:
                    # Генерим ZIP архив для текущего прокси
                    index = line.find(r'host:')
                    if index > -1:
                        line = line[0: index + 6] + '"'+ip+'"' + ','
                    rez.write(line)
            rez.close()
            os.replace(os.getcwd() + r'\Proxy\rez.js', os.getcwd() + r'\Proxy\newproxies\background.js')
            Actions.compressfiles([os.getcwd()+r'\Proxy\newproxies\background.js',
                           os.getcwd()+r'\Proxy\newproxies\manifest.json'],
                          os.getcwd() + '\\Proxy\\newproxies\\' + ip + '.zip')

    print('Обработано проксей '+str(i))



if generate(os.getcwd()+r'\proxy.txt', os.getcwd()+r'\Proxy\newproxies')==False:
    l.write('Генерация прокси расширений НЕУДАЧНО')
else:
    l.write('Генерация прокси расширений прошла удачно')



