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
    all_id = [os.getenv('TG_TWOCHATID')]
    
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
    url = ['4747357','880050516240','4747522','880044225097','880046380236','4747319','4747427','4447352','4321335','880050678110','880049323224',
           '880048550763','880048986442','880044448765','880044516771','880046709117','4226253','4321338','880048044502']

    name = ['Urmart','iherb','KKday(體驗與票券)','Klook(體驗與票券)','寶雅','小三美日','家樂福','屈臣氏','PChome 24h購物','蝦皮特選_官方直營','日藥本舖',
            'KFC 肯德基','Pizza Hut 必勝客','Apple 官方網站','i3fresh 愛上新鮮','特力屋','生活市集','東森購物','金車']

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
    # LineNotify(os.getenv('LINE_USER_ID'), msg) # 單獨的 Line Notify
    # LineNotify(os.getenv('LINE_GROUP_SELF'), msg) # 倆人群

    # 由 Telegram Bot 發送
    send_message_to_telegram(msg) # Telegram兩人群
