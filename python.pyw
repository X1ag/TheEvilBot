import ctypes
import datetime
import json
import os
import platform as pf
import time
import psycopg2 as pg
import cv2
import pyautogui as pag
import requests
import telebot
from telebot import types

token = ''
bot = telebot.TeleBot(token)
open_weather_token = '0240bf3a21fa9bf9c2c413c1ccc6c22e'
myId = ''
conn = pg.connect(database='postgres', user='postgres', password='qwerty', host='127.0.0.1', port='5432')
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT UNIQUE
    );
""")

conn.commit()

cur.close()
conn.close()


def get_usd():
    req = requests.get('http://api.currencylayer.com/live?access_key=7fe2ed73dbae3284b2086b88a6a3d992')
    # Делаем API запрос на цену на все валюты
    response = req.json()
    sell_price = response['quotes']['USDRUB']  # Достаем оттуда цену
    sell_price = int(sell_price * 100) / 100
    return sell_price


requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage?chat_id={myId}&text=Здравствуй хозяин!\nЯ запущен в: {datetime.datetime.now().strftime('%H:%M %d.%m.%Y')}\nКурс доллара: {get_usd()} рублей.")


# Функция при команде /start

def caller(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = ['/ip', '/spec', '/screenshot', '/webcam',
            '/message', '/input', '/wallpaper', '/off', '/sleep', '/request', '/website',
            '/USD', '/ton', '/weather', '/file', '/folder', ]  # Список с кнопками

    for btn in btns:  # Дабы не писать миллион строк кода проходимся циклом по массиву и добавляем каждую кнопку в список кнопок
        rmk.add(types.KeyboardButton(btn))


@bot.message_handler(commands=['db'])
def db(message):
    try:
        conn = pg.connect(database='postgres', user='postgres', password='qwerty', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute("""
            SELECT chat_id FROM users WHERE chat_id=%s""", (message.chat.id,));
        result = cur.fetchone()
        if result is None:
            cur.execute("INSERT INTO users(chat_id) VALUES (%s)", (message.chat.id,));
            conn.commit()
            bot.send_message(message.chat.id, 'Вы успешно зарегистрировались в базе данных!')
        else:
            bot.send_message(message.chat.id, 'Ваш chat_id уже есть в базе данных!')
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, f"Произошла ошибка при регистрации пользователя {message.chat.first_name}")


@bot.message_handler(commands=['start'])
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = ['/ip', '/spec', '/screenshot', '/webcam',
            '/message', '/input', '/wallpaper', '/off', '/sleep', '/request', '/website',
            '/USD', '/ton', '/weather', '/file', '/folder', ]  # Список с кнопками
    #
    for btn in btns:  # Дабы не писать миллион строк кода проходимся циклом по массиву и добавляем каждую кнопку в список кнопок
        rmk.add(types.KeyboardButton(btn))
    bot.send_message(message.chat.id, 'Выберите команду'.format(message.from_user), reply_markup=rmk)


@bot.message_handler(commands=['ton'])
def get_ton(message):
    try:
        req = requests.get(
            'https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true')
        req2 = requests.get('http://api.currencylayer.com/live?access_key=7fe2ed73dbae3284b2086b88a6a3d992')
        data = req.text
        parse_json = json.loads(data)
        active_case = parse_json['the-open-network']['usd']
        response = req2.json()
        sell_price = response['quotes']['USDRUB']
        sell_price = int(sell_price * 100) / 100
        ton_price = round(float(active_case) * float(sell_price), 2)
        bot.send_message(message.chat.id,
                         f'Сейчас {datetime.datetime.now().strftime("%d-%m-%y, %H:%M")}\nТон стоит: {ton_price}')
    except Exception as ex:
        print(ex)

    caller(message=message)


@bot.message_handler(commands=['folder'])
def choose_name(message):
    name_folder = bot.send_message(message.chat.id, 'Введите название папки')
    bot.register_next_step_handler(name_folder, create_folder)


def create_folder(message):
    try:
        os.mkdir(rf"C:\Users\X1ag\forbot{message.text}")
        bot.send_message(message.chat.id, 'Папка создана!')
    except Exception as ex:
        print(ex)
        bot.send_message(message.chat.id, 'Папка с таким названием уже существует!')

    caller(message=message)


@bot.message_handler(commands=['file'])
def get_folder(message):
    try:
        path = r'C:\Users\X1ag\forbot'
        photos = []
        photos2 = []
        photos.append(os.listdir(path=path))
        for i in photos:
            for j in i:
                photos2.append(str(j))
        if '000.jpg' or 'cam.jpg' in photos2:
            print(photos)
            print(photos2)
            photos2.remove('000.jpg') or photos2.remove('cam.jpg')
        else:
            pass
        mesg = bot.send_message(message.chat.id, 'Пришлите название папки')
        bot.send_message(message.chat.id, rf'Вот все папки: {photos2}')
        bot.register_next_step_handler(mesg, get_name)
    except Exception as ex:
        print(ex)


def get_name(message):
    try:
        global name_f
        path = r'C:\Users\X1ag\forbot'
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


def get_photo(message):
    file = message.photo[-1].file_id
    file = bot.get_file(file)
    dfile = bot.download_file(file.file_path)
    timestr = time.strftime("%Y-%m-%d_%H-%M-%S")

    with open(rf'C:\Users\X1ag\forbot\{name_f}\{timestr}' + '.jpg',
              'wb') as timestr:
        timestr.write(dfile)
        bot.send_message(message.chat.id, 'Фото сохранено =)')
    caller(message=message)


@bot.message_handler(commands=['ip', 'ip_address'])
def ip_address(message):
    response = requests.get(
        'http://jsonip.com/').json()  # Делаем запрос на сайт который показывает ip и парсим json
    bot.send_message(message.chat.id, f'Your ip address: {response["ip"]}')
    caller(message=message)


@bot.message_handler(commands=['spec'])
def spec(message):
    msg = f'Name PC: {pf.node()}\nProcessor: i5 8300H, 4 cores, 2.4 GHz\nSystem: {pf.system()} {pf.release()}\nVideocard: Gtx GeForce 1060\nRAM: 8 Gb'
    bot.send_message(message.chat.id, msg)
    caller(message=message)


@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    # Делаем скриншот и сохраняем в определенную директорию, дабы не засорять нынешнюю.
    try:
        pag.screenshot(r'C:\Users\X1ag\forbot\000.jpg')
        with open(r'C:\Users\X1ag\forbot\000.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)
    except Exception as ex:
        print(ex)
    caller(message=message)


@bot.message_handler(commands=['webcam'])
def webcam(message):
    try:
        path = r'C:\Users\X1ag\forbot\cam.jpg'
        if os.path.exists(path):
            os.remove(path)
        else:
            pass

        cap = cv2.VideoCapture(0)
        # Прогреваем камеру
        for i in range(30):
            cap.read()

        ret, frame = cap.read()
        cv2.imwrite(r'C:\Users\X1ag\forbot\cam.jpg', frame)
        cap.release()

        with open(r'C:\Users\X1ag\forbot\cam.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)

    except Exception as ex:
        print(ex)
    caller(message=message)


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
    caller(message=message)


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

    caller(message=message)


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

        with open(r'C:\Users\X1ag\forbot\image.jpg', 'wb') as img:
            img.write(dfile)

        path = os.path.abspath(r'C:\Users\X1ag\forbot\image.jpg')
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        bot.send_message(message.chat.id, 'Обои изменены!')
    except Exception as ex:
        print(ex)
        bot.send_message(message.chat.id, 'Видимо, это не картинка')
    caller(message=message)


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
        # Кнопки с выбором (пользователь может случайно нажать на команду)
        markup_inline = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        item_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        # Добавляем кнопки в бота
        markup_inline.add(item_yes, item_no)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выключить ноутбук?', reply_markup=markup_inline)
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
    try:
        os.system('start https://www.google.com/search?q={}'.format(f'{message.text}'))
        # Делаем гугл запрос с помощью библиотеки
        countdown(2)  # Ставим задержку перед отправкой чтобы страница успела прогрузиться
        pag.screenshot(r'C:\Users\X1ag\forbot\000.jpg')

        # Отправляем файл
        with open(r'C:\Users\X1ag\forbot\000.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)
    except Exception as ex:
        print(ex)
    caller(message=message)


@bot.message_handler(commands=['website'])
def get_website(message):
    # Мой сайт. Команда сделана лишь для кол-ва команд
    bot.send_message(message.chat.id, 'Вот ссылочка :)')
    bot.send_message(message.chat.id, 'https://x1ag.github.io/mywebsite1/')
    caller(message=message)


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
    caller(message=message)


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
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}'
        )
        data = r.json()  # Преобразуем в json файл для более простого извлечения данных
        city = data['name']

        weather_description = data['weather'][0]['main']
        # Ищем названия чтобы поставить смайлики
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, я не понимаю что там за погода!'

        cur_weather = data['main']['temp']  # Температура
        humidity = data['main']['humidity']  # Влажность
        pressure = data['main']['pressure']  # Давление
        wind_speed = data['wind']['speed']  # Скорость ветра
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])  # Восход солнца
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])  # Закат солнца
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

    caller(message=message)


# Счетчик секунд(для запроса в гугл)
def countdown(num_of_secs):
    while num_of_secs:
        m, s = divmod(num_of_secs, 60)
        min_sec_format = '{:02d}:{:02d}'.format(m, s)
        time.sleep(1)
        num_of_secs -= 1


try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    with open(r'C:\Users\X1ag\forbot\log.txt', 'w') as f:
        f.write(f'{e}' + '\n')
