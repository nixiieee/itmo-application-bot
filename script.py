from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep


def get_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    driver.get(url)

    sleep(1)

    html = driver.page_source
    driver.close()
    driver.quit()
    return html

def find_num(page, your_snils):
    #r = open(page).read()
    #soup = bs(r, 'lxml')
    soup = bs(get_html(page), 'lxml')
    t = soup.find_all('div', class_='RatingPage_table__nameBlock__20POr')
    allparts = {}
    for parts in t:
        curpar = parts.find_all('p')
        snils = curpar[1].text
        num = curpar[0].text[:-1]
        if snils == your_snils:
            return num
        allparts[snils] = num

    return "-"

def make_programm_list(page):
    soup = bs(get_html(page), 'lxml')
    t = soup.find_all('div', class_='RatingPage_table__nameBlock__20POr')
    allparts = {}
    for parts in t:
        curpar = parts.find_all('p')
        snils = curpar[1].text
        num = curpar[0].text[:-2]
        allparts[snils] = num
    return allparts

def get_all_lists():
    lists = ["15997", "15998", "15999", "16000", "16025"]
    programms_lists = {}
    for programm_name in lists:
        programms_lists[programm_name] = make_programm_list("https://abit.itmo.ru/rating/bachelor/budget/"+programm_name)
    return programms_lists

def get_num(your_snils):
    #print("Введите ваш ID")
    #your_snils = input()
    programms = {"01.03.02 Прикладная математика и информатика" : "15997",
                "09.03.01 Информатика и вычислительная техника" : "15998",
                "09.03.02 Информационные системы и технологии" : "15999",
                "09.03.03 Прикладная информатика" : "16000",
                "09.03.04 Программная инженерия" : "16025"}
    output = "Твой номер в списках на поступление на направления: \n"
    for programm_name in programms:
        output += programm_name + " : " + find_num("https://abit.itmo.ru/rating/bachelor/budget/"+programms[programm_name], your_snils) + " \n"
    return output



