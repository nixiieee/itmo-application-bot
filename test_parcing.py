from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs

class Applicant:
    def __init__(self, num, category, priority, passport, consent):
        self.num = num
        self.category = category
        self.priority = priority
        self.passport = passport
        self.consent = consent

def get_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

    driver.get(url)

    sleep(2)

    html = driver.page_source

    driver.close()
    driver.quit()

    return html

def find_cat(page):
    soup = bs(page, 'lxml')
    t = soup.find_all('div', class_='RatingPage_table__fMs6t')
    allcats = []
    for cat in t:
        num = cat.find_all('div', class_='RatingPage_table__item__iH7yd')
        allcats.append(len(num))
    return allcats

def find_appl(page, cats):
    soup = bs(page, 'lxml')
    t = soup.find_all('div', class_='RatingPage_table__item__iH7yd')
    allappl = {}
    for applicant in t:
        position_and_snils = applicant.find_all('div', class_='RatingPage_table__nameBlock__20POr')
        curpar = position_and_snils[0].find_all('p')
        snils = curpar[1].text
        position = curpar[0].text[:-1]
        rest1 = applicant.find_all('div', class_='RatingPage_table__info__2gWiU')
        rest2 = rest1[0].find_all('p')
        rest3 = rest1[1].find_all('p')
        rest_fin = rest2 + rest3
        for data in rest_fin:
            cur_data = data.text
            if cur_data[:3] == "При":
                priority = cur_data[-1]
            if cur_data[:3] == "Сог":
                consent = (cur_data[-2:] == "да")
            if cur_data[:3] == "Ори":
                passport = (cur_data[-2:] == "да")
        last = 0
        for j in range(len(cats)):
            if int(position) <= (cats[j] + last):
                category = j
                break
            last += cats[j]
        new_applicant = Applicant(position, category, priority, passport, consent)
        allappl[snils] = new_applicant
    return allappl


page = get_html("https://abit.itmo.ru/rating/bachelor/budget/15997")
cats = find_cat(page)
print(find_appl(page, cats))