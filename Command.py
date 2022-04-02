from fuzzywuzzy import fuzz
import datetime
from os import system
import sys
from random import choice
import webbrowser


def time(self):
    now = datetime.datetime.now()
    self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))


def opener(self, task):
    links = {
        ('браузер', 'интернет', 'browser'): 'https://google.com/',
        ('почта', 'почту', 'gmail', 'гмейл', 'гмеил', 'гмаил'): 'http://gmail.com/',
    }
    j = 0
    if 'и' in task:
        task = task.replace('и', '').replace('  ', ' ')
    double_task = task.split()
    if j != len(double_task):
        for i in range(len(double_task)):
            for vals in links:
                for word in vals:
                    if fuzz.ratio(word, double_task[i]) > 75:
                        webbrowser.open(links[vals])
                        self.talk('Открываю ' + double_task[i])
                        j += 1
                        break


def quite(self):
    self.talk(choice(['Надеюсь мы скоро увидимся', 'Рада была помочь', 'Пока пока', 'Я отключаюсь']))
    self.engine.stop()
    system('cls')
    sys.exit(0)


def shut(self):
    self.talk("Подтвердите действие!")
    text = self.listen()
    print(text)
    if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, "подтверждаю") > 60):
        self.talk('Действие подтверждено')
        self.talk('До скорых встреч!')
        system('shutdown /s /f /t 10')
        self.quite()
    elif fuzz.ratio(text, 'отмена') > 60:
        self.talk("Действие не подтверждено")
    else:
        self.talk("Действие не подтверждено")


def hello(self):
    self.talk(choice(['Привет, чем могу помочь?', 'Здраствуйте', 'Приветствую']))

