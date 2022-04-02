import pyttsx3
import speech_recognition as sr
from pyowm.utils.config import get_default_config
import configparser

import Command
from Command import *


class Assistant:
    settings = configparser.ConfigParser()  # синтаксический анализатор файлов конфигурации
    settings.read('settings.ini')

    config_dict = get_default_config()  # Инициализация get_default_config()
    config_dict['language'] = 'ru'  # Установка языка

    def __init__(self):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()  # получает голос, чтобы передать на сервера гугл
        self.text = ''
        self.cmds = {
            ('текущее время', 'сейчас времени', 'который час'): Command.time,
            ('привет', 'добрый день', 'здравствуй'): Command.hello,
            ('пока', 'вырубись'): Command.quite,
            ('выключи компьютер', 'выруби компьютер'): Command.shut,
        }

        self.ndels = ['помощник', 'ассистент', 'помоги', 'ладно', 'не могла бы ты', 'пожалуйста',
                      'текущее', 'сейчас']

        self.commands = [
            'текущее время', 'сейчас времени', 'который час',
            'открой браузер', 'открой интернет', 'запусти браузер',
            'привет', 'добрый день', 'здравствуй',
            'пока', 'вырубись',
            'выключи компьютер', 'выруби компьютер',
        ]

        self.num_task = 0
        self.j = 0
        self.ans = ''

    def listen(self):
        with sr.Microphone() as source:  # возьми микрофон как источни
            print("Я вас слушаю...")
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)  # слушаем аудио
            try:
                self.text = self.r.recognize_google(audio, language="ru-RU").lower()
            # except Exception as e:
            #     print(e)
            except sr.UnknownValueError:  # если не получилось распознать, что мы сказали
                return 'Listening error'
            except sr.RequestError as e:  # если что-то пошло не так с соединением
                return 'Connecting error'
            return self.text

    def talk(self, text):
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def cleaner(self, text):
        self.text = text

        for i in self.ndels:
            self.text = self.text.replace(i, '').strip()
            self.text = self.text.replace('  ', ' ').strip()

        self.ans = self.text

        for i in range(len(self.commands)):
            k = fuzz.ratio(text, self.commands[i])
            if (k > 70) & (k > self.j):
                self.ans = self.commands[i]
                self.j = k

        return str(self.ans)

    def recognizer(self):
        self.text = self.cleaner(self.listen())
        print(self.text)

        if self.text.startswith(('открой', 'запусти', 'зайди', 'зайди на')):
            Command.opener(self.text)

        for tasks in self.cmds:
            for task in tasks:
                if fuzz.ratio(task, self.text) >= 80:
                    self.cmds[tasks]()

        self.engine.runAndWait()
        self.engine.stop()


if __name__ == '__main__':  # текущий файл нзв мэйн, то выполняем код
    while True:  # пока программа не закроется, выполняем следующие команды
        Assistant().recognizer()
