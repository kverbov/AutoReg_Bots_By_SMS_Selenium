# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC

class Navigate(ABC):

    driver=None

    @abstractmethod
    def logIn(self):
        print('Этот метод - логинимся на сайт')

    @abstractmethod
    def __del__(self):
        if(self.driver!=None):
            # Деструктор - Уничтожения объекта
            self.driver.quit()