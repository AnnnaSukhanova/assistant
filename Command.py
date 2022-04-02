from fuzzywuzzy import fuzz
import datetime
from os import system
import sys
from random import choice
import webbrowser


def hello(self):  # здоровается
    self.say(choice(['Привет, чем могу помочь?', 'Здравствуйте', 'Приветствую']))  # выбирает один из вариантов


def time(self):  # говорит текущее время
    now = datetime.datetime.now()
    self.say("Сейчас " + str(now.hour) + ":" + str(now.minute))


def opener(self, task):  # открывает интернет/почту, потом можно добавить больше ресурсов
    links = {
        ('браузер', 'интернет', 'browser'): 'https://google.com/',
        ('почта', 'почту', 'gmail', 'гмейл', 'гмеил', 'гмаил'): 'http://gmail.com/',
    }
    j = 0
    if 'и' in task:
        task = task.replace('и', '').replace('  ', ' ')
    double_task = task.split()  # разбивает задание на отдельные строки
    if j != len(double_task):  # чтобы была возможность выполнить несколько действий сразу
        for i in range(len(double_task)):
            for vals in links:
                for word in vals:
                    if fuzz.ratio(word, double_task[i]) > 75:
                        webbrowser.open(links[vals])
                        self.say('Открываю ' + double_task[i])
                        j += 1
                        break


def finish(self):  # завершение работы помощника
    self.say(choice(['Надеюсь мы скоро увидимся', 'Рада была помочь', 'Пока пока', 'Я отключаюсь']))
    self.engine.stop()
    system('cls')
    sys.exit(0)


def comp_off(self):
    self.say("Подтвердите действие!")
    text = self.listen()
    if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, "подтверждаю") > 60):
        self.say('Действие подтверждено')
        self.say('До скорых встреч!')
        system('shutdown /s /f /t 10')
        self.finish()
    elif fuzz.ratio(text, 'отмена') > 60:
        self.say("Действие не подтверждено")
    else:
        self.say("Действие не подтверждено")
