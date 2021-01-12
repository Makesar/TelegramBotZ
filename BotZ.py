import telebot
import schedule
import time
from bs4 import BeautifulSoup
import requests as req

##Парсинг гороскопа
def GoroskopMessage():
    resp = req.get("https://horo.mail.ru/prediction/leo/today/")
    soup = BeautifulSoup(resp.text, "lxml")
    tags = soup.find_all('p')
    goroskop ='<b>Гороскоп-' + (soup.find('span', class_='link__text')).text + ':\n</b>'
    #print((soup.find('span', class_='link__text')).text)
    for tag in tags:
        #print(" ".join(tag.text.split()))
        goroskop = goroskop + " ".join(tag.text.split())
    #print(goroskop)
    return goroskop

##Парсинг погоды
resp1 = req.get("https://ru-meteo.ru/saratov/hour")
soup1 = BeautifulSoup(resp1.text, "lxml")
tags1 = soup1.find_all('tbody')[0]
result = []
for tag in tags1:
    list2 = tag.text.split('\n')
    list2 = [x for x in list2 if x]
    list3 = []
    list3.append(list2[0])
    list3.append(list2[1])
  #  list3.append(list2[3]) # Скорость ветра
    result.append(list3)
for res in result:
    temp = res[0]
    temp = temp[5:11]
    res[0] = res[0][0:5] + ' ' + temp

def CreatWeatherMessage(): #Переформатирование сообщения о погоде
    out = '<b>Погода на сегодня: \n</b>'
    for i in result:
        out = out + str(i[0]) + ' ' + str(i[1]) + '\n'
    return out

##Парсинг фото дня
def ImageOfDay():
    resp2 = req.get("https://photosight.ru/")
    soup2 = BeautifulSoup(resp2.text, "lxml")
    tags2 = soup2.find_all('div', class_="gallery-layout")
    fotourl = str(tags2[1])
    a = int(fotourl.index("'"))
    b = int(fotourl.rindex("'"))
    fotourl = fotourl[a+1:b]
    out = '<a href = "' + fotourl + '"> Фото дня: </a>'
    return out

def FinalMessage():
    out = GoroskopMessage() + '\n \n \n' + CreatWeatherMessage() + '\n \n' + ImageOfDay()
    return out

##Телеграм-бот
bot = telebot.TeleBot('1309403639:AAHc3XpngH6UjAwXX3cYRpQ3OFmakIj1zj8')
userid = 388368780

# @bot.message_handler(commands=['start'])
# def welcome_start(message):
#     userid = message.chat.id
#     print(userid)
#     bot.send_message(message.chat.id, 'Привет, Артем!')
#
# @bot.message_handler(commands=['help'])
# def welcome_help(message):
#     bot.send_message(message.chat.id, 'Чем я могу тебе помочь?')
def SendMessage():
    bot.send_message(userid, parse_mode = 'html', text = {FinalMessage()} )

SendMessage()
# schedule.every().day.at("20:30").do(SendMessage) #00:30
# schedule.every().day.at("21:58").do(SendMessage) #01:58
# schedule.every().day.at("22:30").do(SendMessage) #02:30
# schedule.every().day.at("23:58").do(SendMessage) #03:58
# schedule.every().day.at("02:00").do(SendMessage) #06:00
# schedule.every().day.at("05:00").do(SendMessage) #09:00
# schedule.every().day.at("10:00").do(SendMessage) #14:00
# schedule.every().day.at("19:00").do(SendMessage) #23:00
while True:
    schedule.run_pending()
    time.sleep(1)

bot.polling(none_stop=True, interval=0)


