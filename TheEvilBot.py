import requests
import datetime
import cv2 as cv
import ctypes
import time
import pyautogui as pag
import platform as pf
import os
import telebot
from telebot import types
import webbrowser
from config import *
from PyQt5 import QtGui
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QHBoxLayout, QLabel
import sys

token = token

bot = telebot.TeleBot(token)
open_weather_token = open_weather_token


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'Злой бот'
        self.left = 500
        self.top = 200
        self.width = 300
        self.height = 250
        self.iconName = 'icon.ico'

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        hbox = QHBoxLayout()

        self.lineedit = QLineEdit(self)
        self.lineedit.setFont(QtGui.QFont('Sanserif', 12))
        self.lineedit.returnPressed.connect(self.on_pressed)
        hbox.addWidget(self.lineedit)

        self.label = QLabel(self)
        self.label.setText('Введите чат айди и нажмите enter')
        self.label.setFont(QtGui.QFont('Sanserif', 10))
        self.label.adjustSize()
        self.label.move(20, 80)

        self.label = QLabel(self)
        self.label.setFont(QtGui.QFont('Sanserif', 12))
        hbox.addWidget(self.label)

        self.setLayout(hbox)

        self.show()

    def on_pressed(self):
        self.chat = self.lineedit.text()
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage?chat_id={self.chat}&text=Выбери команду: /ip, /spec, /screenshot,"
            f" /webcam, /message, /input, /wallpaper, /off, /sleep, /request, /website, /USD, /weather, /file, /folder")

        # Функция при команде /start
        @bot.message_handler(commands=['start'])
        def start(message):
            rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btns = ['/ip', '/spec', '/screenshot', '/webcam',
                    '/message', '/input', '/wallpaper', '/off', '/sleep', '/request', '/website',
                    '/USD', '/weather', '/file', '/folder', ]  # Список с кнопками

            for btn in btns:  # Дабы не писать миллион строк кода проходимся циклом по массиву и добавляем каждую кнопку в список кнопок
                rmk.add(types.KeyboardButton(btn))

            bot.send_message(message.chat.id, 'Выберите команду', reply_markup=rmk)

        @bot.message_handler(commands=['folder'])
        def choose_name(message):
            name_folder = bot.send_message(message.chat.id, 'Введите название папки')
            bot.register_next_step_handler(name_folder, create_folder)

        def create_folder(message):
            try:
                os.mkdir(rf'C:\Users\x1ag\Desktop\forbot\{message.text}')
                bot.send_message(message.chat.id, 'Папка создана!')
            except Exception as ex:
                print(ex)

        @bot.message_handler(commands=['file'])
        def get_folder(message):
            try:
                path = r'C:\Users\x1ag\Desktop\forbot'
                photos = []
                photos2 = []
                photos.append(os.listdir(path=path))
                for i in photos:
                    for j in i:
                        photos2.append(j)
                if '000.jpg' or 'cam.jpg' in photos2:
                    photos2.remove('000.jpg') or photos2.remove('cam.jpg')
                else:
                    pass
                mesg = bot.send_message(message.chat.id, 'Пришлите название папки')
                bot.send_message(message.chat.id, rf'Вот все папки: {photos2}')
                bot.register_next_step_handler(mesg, get_name)
            except Exception as ex:
                print(ex)
                print('Я в get_folder')

        def get_name(message):
            try:
                global name_f
                path = r'C:\Users\x1ag\Desktop\forbot'
                name_f = message.text
                if os.path.exists(rf'{path}\{message.text}'):
                    pass
                else:
                    bot.send_message(message.chat.id, 'Такой папки нет')
                    return
                msg = bot.send_message(message.chat.id, 'Пришли фото, которое надо сохранить')
                bot.register_next_step_handler(msg, get_photo)
            except Exception as ex:
                print(ex)
                print('Я в get_name')

        def get_photo(message):
            file = message.photo[-1].file_id
            file = bot.get_file(file)
            dfile = bot.download_file(file.file_path)
            timestr = time.strftime("%Y-%m-%d_%H-%M-%S")

            with open(rf'C:\Users\x1ag\Desktop\forbot\{name_f}\{timestr}' + '.jpg', 'wb') as timestr:
                timestr.write(dfile)
                bot.send_message(message.chat.id, 'Фото сохранено =)')

        @bot.message_handler(commands=['ip', 'ip_address'])
        def ip_address(message):
            response = requests.get(
                'http://jsonip.com/').json()  # Делаем запрос на сайт который показывает ip и парсив json формат
            bot.send_message(message.chat.id, f'Your ip address: {response["ip"]}')

        @bot.message_handler(commands=['spec'])
        def spec(message):
            msg = f'Name PC: {pf.node()}\nProcessor: i5 8300H, 4 cores, 2.4 GHz\nSystem: {pf.system()} {pf.release()}\nVideocard: Gtx GeForce 1060\nRAM: 8 Gb'
            bot.send_message(message.chat.id, msg)

        @bot.message_handler(commands=['screenshot'])
        def screenshot(message):
            # Делаем скриншот и сохраняем в определенную директорию, дабы не засорять нынешнюю.
            pag.screenshot(r'C:\Users\x1ag\Desktop\forbot\000.jpg')

            with open(r'C:\Users\x1ag\Desktop\forbot\000.jpg', 'rb') as img:
                bot.send_photo(message.chat.id, img)

        @bot.message_handler(commands=['webcam'])
        def webcam(message):
            cap = cv.VideoCapture(0)
            # Прогреваем камеру
            for i in range(30):
                cap.read()

            ret, frame = cap.read()

            cv.imwrite(r'C:\Users\x1ag\Desktop\forbot\cam.jpg', frame)
            cap.release()

            with open(r'C:\Users\x1ag\Desktop\forbot\cam.jpg', 'rb') as img:
                bot.send_photo(message.chat.id, img)

        @bot.message_handler(commands=['message'])
        def message_sending(message):
            msg = bot.send_message(message.chat.id, 'Введите ваше сообщение')
            bot.register_next_step_handler(msg, next_message_sending)

        def next_message_sending(message):
            try:
                pag.alert(message.text, '^')
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, 'Что-то пошло не так')

        @bot.message_handler(commands=['input'])
        def message_sending_with_input(message):
            msg = bot.send_message(message.chat.id, 'Введите ваше сообщение')
            bot.register_next_step_handler(msg, next_message_sending_with_input)

        def next_message_sending_with_input(message):
            try:
                # Чтобы бот не слетел делаем проверку try except
                answer = pag.prompt(message.text, '^')
                # Бот вызывает на компьютере команду которая подразумевает под собой ответ, собственно этот ответ мы и выводим
                bot.send_message(message.chat.id, answer)
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, 'Что-то пошло не так')

        @bot.message_handler(commands=['wallpaper'])
        def wallpaper(message):
            msg = bot.send_message(message.chat.id, 'Отправьте картинку')
            bot.register_next_step_handler(msg, next_wallpaper)

        @bot.message_handler(content_types=['photo'])
        def next_wallpaper(message):
            try:
                file = message.photo[-1].file_id
                file = bot.get_file(file)
                dfile = bot.download_file(file.file_path)

                with open(r'C:\Users\x1ag\Desktop\forbot\image.jpg', 'wb') as img:
                    img.write(dfile)

                path = os.path.abspath(r'C:\Users\x1ag\Desktop\forbot\image.jpg')
                ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, 'Видимо, это не картинка')

        @bot.message_handler(commands=['off'])
        def off(message):
            # Кнопки с выбором (пользователь может случайно нажать на команду)
            markup_inline = types.InlineKeyboardMarkup()
            item_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
            item_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
            # Добавляем кнопки в бота
            markup_inline.add(item_yes, item_no)
            bot.send_message(message.chat.id, 'Выключить ноутбук?', reply_markup=markup_inline)

        @bot.callback_query_handler(func=lambda call: True)
        def calldata(call):
            if call.data == 'yes':
                # Если да, то выключаем
                os.system("shutdown /p")
                # Если нет, то ничего не делаем
            elif call.data == 'no':
                pass

        @bot.message_handler(commands=['sleep'])
        def sleep(message):
            bot.send_message(message.chat.id, 'Переключаю ноутбук в режим сна')
            # Специальный файл для подобия сна у компьютера
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        @bot.message_handler(commands=['request'])
        def get_request(message):
            msg = bot.send_message(message.chat.id, 'Какой запрос хотите сделать?')
            # Используем технологию next_step_handler
            bot.register_next_step_handler(msg, next_request)

        def next_request(message):
            webbrowser.open_new_tab('https://www.google.com/search?q={}'.format(f'{message.text}'))
            # Делаем гугл запрос с помощью библиотеки
            countdown(5)  # Ставим задержку перед отправкой чтобы страница успела прогрузиться
            pag.screenshot(r'C:\Users\x1ag\Desktop\forbot\000.jpg')

            # Отправляем файл
            with open(r'C:\Users\x1ag\Desktop\forbot\000.jpg', 'rb') as img:
                bot.send_photo(message.chat.id, img)

        @bot.message_handler(commands=['website'])
        def get_website(message):
            # Мой сайт. Команда сделана лишь для кол-ва команд
            bot.send_message(message.chat.id, 'Вот ссылочка :)')
            bot.send_message(message.chat.id, 'https://x1ag.github.io/mywebsite1/')

        @bot.message_handler(commands=['USD', 'usd'])
        def get_data(message):
            req = requests.get('http://api.currencylayer.com/live?access_key=7fe2ed73dbae3284b2086b88a6a3d992')
            # Делаем API запрос на цену на все валюты
            response = req.json()
            sell_price = response['quotes']['USDRUB']  # Достаем оттуда цену
            sell_price = int(sell_price * 100) / 100  # Округляем до двух чисел после запятой
            bot.send_message(message.chat.id,
                             # Преобразуем дату для более удобного чтения
                             f'Сейчас {datetime.datetime.now().strftime("%d-%m-%y, %H:%M")}\nДоллар стоит: {sell_price}')

        @bot.message_handler(commands=['weather'])
        def get_weather(message):
            # Просим название города для дальнейшей обработки
            city = bot.send_message(message.chat.id, "Пришлите название города")
            bot.register_next_step_handler(city, show_weather)

        def show_weather(message):
            city = message.text
            code_to_smile = {
                'Clear': "Ясно \U00002600",
                'Clouds': 'Облачно \U00002601',
                'Rain': 'Дождь \U00002614',
                'Drizzle': "Дождь \U00002614",
                'Thunderstorm': 'Гроза \U000026A1',
                'Snow': 'Снег \U0001F328',
                'Mist': 'Туман \U0001F32B',
                # Смайлики для более приятного чтения
            }
            try:
                # Делаем исключения чтобы бот не слетел. Запрашиваем api с данными города
                r = requests.get(
                    f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={open_weather_token}&units=metric'
                )
                data = r.json()  # Преобразуем в json файл для более простого извлечения данных
                lat = data[0]['lat']
                lon = data[0]['lon']
                city = data[0]['name']
                # Получаем координаты города и его название

                # Делаем гет запрос чтобы получить файл со всеми погодными условиями в этом районе
                g = requests.get(
                    f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}'
                    f'&units=metric')
                weather = g.json()

                weather_description = weather['weather'][0]['main']
                # Ищем названия чтобы поставить смайлики
                if weather_description in code_to_smile:
                    wd = code_to_smile[weather_description]
                else:
                    wd = 'Посмотри в окно, я не понимаю что там за погода!'

                cur_weather = weather['main']['temp']  # Температура
                humidity = weather['main']['humidity']  # Влажность
                pressure = weather['main']['pressure']  # Давление
                wind_speed = weather['wind']['speed']  # Скорость ветра
                sunrise_timestamp = datetime.datetime.fromtimestamp(weather['sys']['sunrise'])  # Восход солнца
                sunset_timestamp = datetime.datetime.fromtimestamp(weather['sys']['sunset'])  # Закат солнца
                length_of_the_day = sunset_timestamp - sunrise_timestamp  # Продолжительность дня

                bot.send_message(message.chat.id, f'***{datetime.datetime.now().strftime("%d-%m-%y, %H:%M")}***\n'
                                                  f'Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n'
                                                  f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind_speed}'
                                                  f'м/c\n'
                                                  f'Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n'
                                                  f'Продолжительность дня: {length_of_the_day}\n'
                                                  f'***Хорошего дня!***')

            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, 'Проверьте название города/штата')

        # Счетчик секунд(для запроса в гугл)
        def countdown(num_of_secs):
            while num_of_secs:
                m, s = divmod(num_of_secs, 60)
                min_sec_format = '{:02d}:{:02d}'.format(m, s)
                print(min_sec_format, end='/r')
                time.sleep(1)
                num_of_secs -= 1

        bot.polling()

    def start_bot(self):
        x = QProcess.run(['python', 'TheEvilBot.py'])


# Когда бот включен он пишет такое сообщение пользователю


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
