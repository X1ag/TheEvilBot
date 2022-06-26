import requests
import datetime
import cv2
import ctypes
import time
import pyautogui as pag
import platform as pf
import os
import telebot
from telebot import types
import webbrowser

token = 'here telegrambot token'
chat_id1 = 'user chat id'
bot = telebot.TeleBot(token)
open_weather_token = 'here open_weather_token'

requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id1}&text=Выбери команду: /ip, /spec, /screenshot,"
    f" /webcam, /message, /input, /wallpaper, /off, /restart, /sleep, /request, /website, /USD, /weather")
    # Когда бот включен он пишет такое сообщение пользователю

# Функция при команде /start
@bot.message_handler(commands=['start'])
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = ['/ip', '/spec', '/screenshot', '/webcam',
            '/message', '/input', '/wallpaper', '/off',
            '/restart', '/sleep', '/request', '/website',
            '/USD', '/weather'] # Список с кнопками кнопки

    for btn in btns: # Дабы не писать миллион строк кода проходимся циклом по массиву и добавляем каждую кнопку в список кнопок
        rmk.add(types.KeyboardButton(btn))

    bot.send_message(message.chat.id, 'Выберите команду', reply_markup=rmk)


@bot.message_handler(commands=['ip', 'ip_address'])
def ip_address(message):
    response = requests.get('http://jsonip.com/').json() # Делаем запрос на сайт который показывает ip и парсив json формат
    bot.send_message(message.chat.id, f'Your ip address: {response["ip"]}')


@bot.message_handler(commands=['spec'])
def spec(message):
    msg = f'Name PC: {pf.node()}\nProcessor: {pf.processor()}\nSystem: {pf.system()} {pf.release()}'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    #Делаем скриншот и сохраняем в определенную директорию, дабы не засорять нынешнюю.
    pag.screenshot(r'C:\Users\x1ag\Desktop\forbot\000.jpg')

    with open(r'C:\Users\x1ag\Desktop\forbot\000.jpg', 'rb') as img:
        bot.send_photo(message.chat.id, img)




@bot.message_handler(commands=['webcam'])
def webcam(message):
    cap = cv2.VideoCapture(0)
    # Прогреваем камеру
    for i in range(30):
        cap.read()

    ret, frame = cap.read()

    cv2.imwrite(r'C:\Users\x1ag\Desktop\forbot\cam.jpg', frame)
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
        #Чтобы бот не слетел делаем проверку try except
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
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    markup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, 'Выключить ноутбук?', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def calldata(call):
    if call.data == 'yes':
        os.system("shutdown /p")
    elif call.data == 'no':
        pass


@bot.message_handler(commands=['restart'])
def restart(message):
    markup_inline1 = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='Да', callback_data='yesrestart')
    item_no = types.InlineKeyboardButton(text='Нет', callback_data='norestart')
    markup_inline1.add(item_yes, item_no)
    bot.send_message(message.chat.id, 'Перезагрузить ноутбук?', reply_markup=markup_inline1)


@bot.callback_query_handler(func=lambda call: True)
def calldata1(call):
    if call.data == 'yesrestart':
        os.system("shutdown /r /t 00")
    elif call.data == 'norestart':
        pass


@bot.message_handler(commands=['sleep'])
def sleep(message):
    bot.send_message(message.chat.id, 'Переключаю ноутбук в режим сна')
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    bot.send_message(message.chat.id, 'Ноутбук в режиме сна')


@bot.message_handler(commands=['request'])
def get_request(message):
    msg = bot.send_message(message.chat.id, 'Какой запрос хотите сделать?')
    bot.register_next_step_handler(msg, next_request)


def next_request(message):
    webbrowser.open_new_tab('https://www.google.com/search?q={}'.format(f'{message.text}'))
    #Делаем гугл запрос с помощью библиотеки
    countdown(5) # Ставим задержку перед отправкой чтобы страница успела прогрузиться
    pag.screenshot(r'C:\Users\x1ag\Desktop\forbot\000.jpg')

    with open(r'C:\Users\x1ag\Desktop\forbot\000.jpg', 'rb') as img:
        bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=['website'])
def get_website(message):
    bot.send_message(message.chat.id, 'Сейчас кину ссылочку :)')
    bot.send_message(message.chat.id, 'https://x1ag.github.io/mywebsite1/')


@bot.message_handler(commands=['USD', 'usd'])
def get_data(message):
    req = requests.get('http://api.currencylayer.com/live?access_key=7fe2ed73dbae3284b2086b88a6a3d992')
    # Делаем API запрос на цену на все валюты
    response = req.json()
    sell_price = response['quotes']['USDRUB'] # Достаем оттуда цену
    sell_price = int(sell_price * 100) / 100 # Округляем до двух чисел после запятой
    bot.send_message(message.chat.id,
                     f'Сейчас {datetime.datetime.now().strftime("%d-%m-%y, %H:%M")}\nДоллар стоит: {sell_price}')


@bot.message_handler(commands=['weather'])
def get_weather(message):
    bot.send_message(message.chat.id, "Пришлите название города")


@bot.message_handler(content_types=['text'])
def show_weather(message: types.Message):
    city = message.text
    code_to_smile = {
        'Clear': "Ясно \U00002600",
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': "Дождь \U00002614",
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B',
        # Смайлики
    }
    try:
        r = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={open_weather_token}&units=metric'
        )
        data = r.json()
        lat = data[0]['lat']
        lon = data[0]['lon']
        city = data[0]['name']
        # Получаем координаты города и его название

        g = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}'
            f'&units=metric')
        weather = g.json()
        # Делаем гет запрос чтобы получить файл со всеми погодными условиями в этом районе

        cur_weather = weather['main']['temp']

        weather_description = weather['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, я не понимаю что там за погода!'

        humidity = weather['main']['humidity']
        pressure = weather['main']['pressure']
        wind_speed = weather['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(weather['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(weather['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

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


def countdown(num_of_secs):
    while num_of_secs:
        m, s = divmod(num_of_secs, 60)
        min_sec_format = '{:02d}:{:02d}'.format(m, s)
        print(min_sec_format, end='/r')
        time.sleep(1)
        num_of_secs -= 1
    # Счетчик секунд(для запроса в гугл)


bot.polling()
