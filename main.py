import Assistant
from Assistant import *

if __name__ == '__main__':  # текущий файл нзв мэйн, то выполняем код
    while True:  # пока программа не закроется, выполняем следующие команды
        Assistant.handle_message()  # начинаем обработку запросов
