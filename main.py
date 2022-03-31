import random
import playsound
import pyaudio

from gtts import gTTS
import speech_recognition as sr
from playsound import playsound



def listen():
    r = sr.Recognizer()  # получает голос, чтобы передать на сервера гугл
    with sr.Microphone() as source:  # возьми микрофон как источник
        print("Скажите команду:")
        audio = r.listen(source)  # слушаем аудио
    try:  # будет пытаться распознать текст
        speech = r.recognize_google(audio, language="ru")
        print("Вы сказали:", speech)
        return str(speech)
    except sr.UnknownValueError:  # если не получилось распознать, что мы сказали
        return 'error'
    except sr.RequestError as e:  # если что-то пошло не так с соединением
        return 'error'


def say(text):
    voice = gTTS(text, lang="ru")  # возьмет текст, отправит на сервера гугл, преобразует и вернет звук
    unique_filename = "audio_" + str(random.randint(0, 100000)) + ".mp3"  # создаем уникальное название файла
    voice.save(unique_filename)  # сохраняем полученный звук
    playsound(unique_filename)  # озвучиваем файл

    print("Ассистент:", text)  # все, что сюда передадим, выведется с префиксом "Ассистент"


def handle_message(message):  # обработка команд
    message = message.lower()  # убираем чувствительность к регистру
    if "привет" in message:  # Если содержимое привет присутствует в сообщении
        say("Привет привет")  # то ассистент отвечаeт так
    elif "прощай" in message:  # Если получаем "прощай", то вызываем ф-ию finish
        finish()
    else:  # если команда ассистенту не известна
        say("Я такой команды не знаю")


def finish():  # для остановки программы
    say("Пока")
    exit()


if __name__ == '__main__':  # текущий файл нзв мэйн, то выполняем код

    while True:  # пока программа не закроется, выполняем следующие команды
        command = listen()  # сначала ассистент должен нас слушать, возвращает что-то в качестве текста
        handle_message(command)  # передали на обработку команду
