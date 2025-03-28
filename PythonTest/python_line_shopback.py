#引入使用套件
import requests
import json
import os
from bs4 import BeautifulSoup
import telebot
from linebot.models import TextSendMessage
from linebot import (
    LineBotApi, WebhookHandler
)

# 不讓伺服器當作機器人
header = {
    # 用 text/html 方法，以 UTF-8 格式解析
    'content-type' : 'text/html; charset=UTF-8',
    # 用什麼方式執行(Mozilla、AppleWebKit、Chrome)
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39'}

def line_Shop_give(url):
    # 使用 get 方法與伺服器聯繫
    res = requests.get(url, headers = header)
    # 利用 BeautifulSoup 解析網頁 HTML 資料
    soup = BeautifulSoup(res.text, 'html.parser') # 將網頁資料以 html.parser 方法解析

    # 平台名稱
    name = soup.find('div',{'id':'app'}).find('h1',{'class':'partnerInfo-title'}).find_all('span')[0].text

    try:
        # 取得回饋%%
        giveBack = soup.find('div',{'id':'app'}).find('span',{'class':'partnerInfo-offerPoint'}).text

        return giveBack, name
    except:
        return '0%', name

# LineNotify 應用，需要 token 權杖
def LineNotify(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
                }
    params = {
        "message": msg
                }
    # image = {'imageFile': file}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)#, files = image)

def send_message_to_telegram(message):
    API_TOKEN = os.getenv('TG_MYBOT_TOKEN')
    all_id = [os.getenv('TG_TWOHATID')]
    
    bot = telebot.TeleBot(API_TOKEN)
    for chat_id in all_id:
        bot.send_message(chat_id, message)

#=============================================================================

# Line Notify
if __name__ == "__main__":
    # 網址：line購物Urmart回饋

    # 前段網址固定
    url_basic = 'https://buy.line.me/u/partner/'

    # 各平台回饋之網址變動處
    url = ['4747357','4708167','4747427','880045010715','880045975302','880044516771','880044764273','880044827160','4217685','4747319','880046709117','880048550763',
           '4536567','4536643','880045421194','880044448765','880046791255','880045874010','880044297879','880046380236','880046584873']

    name = ['Urmart','松果購物','家樂福','Myprotein','蝦皮超市','i3fresh','iherb','hahow','台灣樂天市場','小三美日官網','特力屋','肯德基KFC',
            '康是美網購eshop','瓜瓜園','摩曼頓','Apple','亞尼克','一之軒','大樹健康','寶雅','新光三越skm']

    # 儲存回傳之平台名稱
    name_brand = []

    # 儲存回傳之回饋
    give_back = []

    # 儲存line通知資料
    msg = ''

    for i in range(0,len(url)):
        try:
            # 呼叫 function 執行爬蟲，回傳回饋及平台名稱
            back, brand = line_Shop_give(url_basic + url[i])

            # 存入回饋
            give_back.append(back)
            # 存入平台名稱
            name_brand.append(brand)

            # print(str(give_back[i]).rjust(4), brand)
            # 將回饋及平台名稱存成文字串，以方便line方送通知查看
            msg = msg + '\n' + str(give_back[i]).rjust(4) + '\t' + brand# name[i]

        except:
            msg = msg
        
    # 從LINE Notify取得的權杖(token)
    LineNotify(os.getenv('LINE_USER_ID'), msg) # 單獨的 Line Notify
    LineNotify(os.getenv('LINE_GROUP_SELF'), msg) # 倆人群
    # send_message_to_telegram(msg) # Telegram兩人群
