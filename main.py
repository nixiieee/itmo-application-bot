import telebot
from telebot import types
from datetime import datetime
import subprocess
import schedule
import time
import script

programms_lists = {}
cursnils = "0"
flag = False
#subprocess.call("python3 reload.py", shell=True)

def get_nums(your_snils, type, flag):
    global programms_lists
    if not flag:
        programms_lists = script.get_all_lists()
    programms_names = {"01.03.02 Прикладная математика и информатика" : "15997",
                "09.03.01 Информатика и вычислительная техника" : "15998",
                "09.03.02 Информационные системы и технологии" : "15999",
                "09.03.03 Прикладная информатика" : "16000",
                "09.03.04 Программная инженерия" : "16025"}
    vals = list(programms_names.keys())
    output = "Твой номер в списках на поступление на направления: \n"
    if type == 5:
        count = 0
        for programm_name in programms_names:
            if your_snils in programms_lists[programms_names[programm_name]]:
                found_appl = programms_lists[programms_names[programm_name]][your_snils]
                if found_appl[3] and found_appl[4]:
                    output += "<u>" + programm_name + "</u> : \n"
                if found_appl[3] and not(found_appl[4]):
                    output += "<b>" + programm_name + "</b> : \n"
                if found_appl[4] and not(found_appl[3]):
                    output += "<i>" + programm_name + "</i> : \n"
                if not(found_appl[3]) and not(found_appl[4]):
                    output += programm_name + " :\n"
                output += "\t\t\t\tПриоритет: " + str(found_appl[2]) + "\n"
                output += "\t\t\t\tРейтинговый номер: " + str(found_appl[0]) + "\n"
                output += "\t\t\t\tКонкурс:"
                if found_appl[1] == 0:
                    output += " БВИ\n"
                elif found_appl[1] == 1:
                    output += " Целевая квота\n"
                elif found_appl[1] == 2:
                    output += " Особая квота\n"
                elif found_appl[1] == 3:
                    output += " Специальная квота\n"
                elif found_appl[1] == 4:
                    output += " Общий конкурс\n"
            else:
                count += 1
        if count == 5:
            output = "Данные о твоей заявке не найдены :("
        else:
            output += "\n<i>Курсив</i> = согласие на зачисление, <b>жирный</b> = оригинал документа, <u>подчеркнутый</u> = согласие и оригинал одновременно."
            output += "\n<i>via @ITMOAdmissionBot at " + str(datetime.now())[:-7] + "</i>"
    else:
        programm_name = vals[type]
        if your_snils in programms_lists[programms_names[vals[type]]]:
            found_appl = programms_lists[programms_names[programm_name]][your_snils]
            if found_appl[3] and found_appl[4]:
                output += "<u>" + programm_name + "</u> : \n"
            if found_appl[3] and not (found_appl[4]):
                output += "<b>" + programm_name + "</b> : \n"
            if found_appl[4] and not (found_appl[3]):
                output += "<i>" + programm_name + "</i> : \n"
            if not (found_appl[3]) and not (found_appl[4]):
                output += programm_name + " :\n"
            output += "\t\t\t\tПриоритет: " + str(found_appl[2]) + "\n"
            output += "\t\t\t\tРейтинговый номер: " + str(found_appl[0]) + "\n"
            output += "\t\t\t\tКонкурс:"
            if found_appl[1] == 0:
                output += " БВИ\n"
            elif found_appl[1] == 1:
                output += " Целевая квота\n"
            elif found_appl[1] == 2:
                output += " Особая квота\n"
            elif found_appl[1] == 3:
                output += " Специальная квота\n"
            elif found_appl[1] == 4:
                output += " Общий конкурс\n"
            output += "\n<i>Курсив</i> = согласие на зачисление, <b>жирный</b> = оригинал документа, <u>подчеркнутый</u> = согласие и оригинал одновременно."
            output += "\n<i>via @ITMOAdmissionBot at " + str(datetime.now())[:-7] + "</i>"
        else:
            output = "Данные о твоей заявке не найдены :("
    return output

bot = telebot.TeleBot('5269737355:AAGq7p1GEGiWBB8rzUBz--AQwFmbVGByC-I')
bot.remove_webhook()
joinedFile = open("joined.txt", "r")
joinedUsers = set()
for line in joinedFile:
   joinedUsers.add(line.strip())

@bot.message_handler(commands=['start'])
def start(message):
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("joined.txt", "w")
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Узнать свое место в списках")
    markup.add(btn)
    bot.send_message(message.chat.id, "Привет! Чтобы узнать, на каком месте ты находишься в рейтинговых списках на поступление, нажми на кнопку.", reply_markup=markup)

@bot.message_handler(commands=['special'])
def special(message):
    if message.chat.id == 596114319:
        f = 0
        for user in joinedUsers:
            try:
                bot.send_message(user, message.text[message.text.find(' '):])
            except:
                f = 1
                joinedUsers.remove(user)
    if f == 1:
        joinedFile = open("joined.txt", "w")
        joinedFile.truncate(0)
        for user in joinedUsers:
            joinedFile.write(user + "\n")

@bot.message_handler(content_types=['text'])
def get_user_message(message):
    t = message.text
    global cur_snils
    global flag
    k = ["01.03.02 Прикладная математика и информатика", "09.03.01 Информатика и вычислительная техника",
         "09.03.02 Информационные системы и технологии", "09.03.03 Прикладная информатика",
         "09.03.04 Программная инженерия", "Все направления"]
    if t == "Узнать свое место в списках" or t == "Вернуться назад":
        bot.send_message(message.chat.id, text="Отправь, пожалуйста, свой номер СНИЛС без пробелов и тире.")
    elif t == "Все направления":
        solution = get_nums(cur_snils, 5, flag)
        flag = True
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif t == "01.03.02 Прикладная математика и информатика":
        solution = get_nums(cur_snils, 0, flag)
        flag = True
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif t == "09.03.01 Информатика и вычислительная техника":
        solution = get_nums(cur_snils, 1, flag)
        flag = True
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif t == "09.03.02 Информационные системы и технологии":
        solution = get_nums(cur_snils, 2, flag)
        flag = True
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif t == "09.03.03 Прикладная информатика":
        solution = get_nums(cur_snils, 3, flag)
        flag = True
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif t == "09.03.04 Программная инженерия":
        solution = get_nums(cur_snils, 4, flag)
        flag = True
        bot.send_message(message.chat.id, solution, parse_mode='html')
    elif (t[0] == "F" and len(t) == 12) or (len(t) == 11 and t.isdecimal()):
        cur_snils = t
        flag = False
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