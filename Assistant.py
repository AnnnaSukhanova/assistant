import colorama
import pyttsx3
import speech_recognition as sr

import Command
from Command import *


def __init__(self):
    self.engine = pyttsx3.init()  # озвучивает системное время и любой текст
    self.r = sr.Recognizer()  # получает голос
    self.text = ''
    self.cmds = {  # на какие слова выполняются какие команды
        ('текущее время', 'сейчас времени', 'который час'): Command.time,
        ('привет', 'добрый день', 'здравствуй'): Command.hello,
        ('пока', 'вырубись'): Command.finish,
        ('выключи ноутбук', 'выруби компьютер', 'выключи компьютер', 'выруби ноутбук'): Command.comp_off,
    }

    self.delete = ['помощник', 'ассистент', 'помоги', 'ладно', 'не могла бы ты', 'пожалуйста',
                   'текущее', 'сейчас']  # какие слова будем удалять из озвученной команды

    self.commands = [  # список слов, на которые будут выполняться какие-либо команды
        'текущее время', 'сейчас времени', 'который час',
        'открой браузер', 'открой интернет', 'запусти браузер',
        'привет', 'добрый день', 'здравствуй',
        'пока', 'вырубись',
        'выключи компьютер', 'выруби компьютер',
    ]

    self.num_task = 0  # номер запроса
    self.j = 0  # счетчик
    self.ans = ''


def listen(self):
    with sr.Microphone() as source:  # возьми микрофон как источник
        print(colorama.Fore.LIGHTWHITE_EX + "Я вас слушаю...")
        self.r.adjust_for_ambient_noise(source)  # настройка посторонних шумов
        audio = self.r.listen(source)  # слушаем аудио
        try:
            self.text = self.r.recognize_google(audio, language="ru-RU").lower()  # пытаемся распознать аудио
            print(colorama.Fore.LIGHTCYAN_EX + "Вы сказали: " + self.text)
        except sr.UnknownValueError:  # если не получилось распознать, что мы сказали
            return 'Listening error'
        except sr.RequestError as e:  # если что-то пошло не так с соединением
            return 'Connecting error'
        return self.text


def say(self, text):
    print(colorama.Fore.LIGHTGREEN_EX + "Ассистент: " + text)  # пишет текст
    self.engine.say(text)  # озвучивает текст
    self.engine.runAndWait()  # чуть ждет


def cleaner(self, text):
    self.text = text

    for i in self.delete:  # для каждого слова из списка на удаление
        self.text = self.text.replace(i, '').strip()
        self.text = self.text.replace('  ', ' ').strip()

    self.ans = self.text  # меняем текст команды на чистый текст

    for i in range(len(self.commands)):
        k = fuzz.ratio(text, self.commands[i])
        if k > 70:
            self.ans = self.commands[i]

    return str(self.ans)  # возвращаем чистую команду


def handle_message(self):
    self.text = self.cleaner(self.listen())  # выделяем в услышанном тексте команды

    if self.text.startswith(('открой', 'запусти', 'зайди', 'зайди на')):  # если начинается с этих слов выполняем
        Command.opener(self.text)  # команду опен

    for tasks in self.cmds:  # для задач из списка команд
        for task in tasks:
            if fuzz.ratio(task, self.text) >= 80:
                self.cmds[tasks]()

    if self.text not in self.commands:
        self.say("я вас не понимаю")

    self.engine.runAndWait()
    self.engine.stop()
