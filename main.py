import telebot
import subprocess
import reload
from telebot import types
import time

programms_lists = {}

subprocess.call("reload.py", shell=True)

def get_nums(your_snils, type):
    programms_lists = reload.get()
    programms_names = {"01.03.02 Прикладная математика и информатика" : "15997",
                "09.03.01 Информатика и вычислительная техника" : "15998",
                "09.03.02 Информационные системы и технологии" : "15999",
                "09.03.03 Прикладная информатика" : "16000",
                "09.03.04 Программная инженерия" : "16025"}
    vals = list(programms_names.keys())
    output = "Твой номер в списках на поступление на направления: \n"
    if type == 5:
        for programm_name in programms_names:
            if your_snils in programms_lists[programms_names[programm_name]]:
                output += programm_name + " : " + programms_lists[programms_names[programm_name]][your_snils] + " \n"
            else:
                output += programm_name + " : -\n"
    else:
        if your_snils in programms_lists[programms_names[vals[type]]]:
            output += vals[type] + " : " + programms_lists[programms_names[vals[type]]][your_snils]
        else:
            output = "Данные о твоей заявке не найдены :("
    return output


bot = telebot.TeleBot('5269737355:AAFJrXBmJyBC4y1P7YeEYNDrABk5lDZe5C8')
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Узнать свое место в списках")
    markup.add(btn)
    bot.send_message(message.chat.id, "Привет! Чтобы узнать, на каком месте ты находишься в рейтинговых списках на поступление, нажми на кнопку.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_user_message(message):
    t = message.text
    global cur_snils
    k = ["01.03.02 Прикладная математика и информатика", "09.03.01 Информатика и вычислительная техника",
         "09.03.02 Информационные системы и технологии", "09.03.03 Прикладная информатика",
         "09.03.04 Программная инженерия", "Все направления"]
    if t == "Узнать свое место в списках" or t == "Вернуться назад":
        bot.send_message(message.chat.id, text="Отправь, пожалуйста, свой номер СНИЛС без пробелов и тире.")
    elif t == "Все направления":
        solution = get_nums(cur_snils, 5)
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif t == "01.03.02 Прикладная математика и информатика":
        solution = get_nums(cur_snils, 0)
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif t == "09.03.01 Информатика и вычислительная техника":
        solution = get_nums(cur_snils, 1)
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif t == "09.03.02 Информационные системы и технологии":
        solution = get_nums(cur_snils, 2)
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif t == "09.03.03 Прикладная информатика":
        solution = get_nums(cur_snils, 3)
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif t == "09.03.04 Программная инженерия":
        solution = get_nums(cur_snils, 4)
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif (t[0] == "F" and len(t) == 12) or (len(t) == 11 and t.isdecimal()):
        cur_snils = t
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("01.03.02 Прикладная математика и информатика")
        btn2 = types.KeyboardButton("09.03.01 Информатика и вычислительная техника")
        btn3 = types.KeyboardButton("09.03.02 Информационные системы и технологии")
        btn4 = types.KeyboardButton("09.03.03 Прикладная информатика")
        btn5 = types.KeyboardButton("09.03.04 Программная инженерия")
        btn6 = types.KeyboardButton("Все направления")
        btn7 = types.KeyboardButton("Вернуться назад")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
        bot.send_message(message.chat.id, text="Выбери направление, которое тебя интересует.", reply_markup=markup)

if __name__ == '__main__':
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)