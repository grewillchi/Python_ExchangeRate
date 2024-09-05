import requests
import os
import json
import socket
import time
from bs4 import BeautifulSoup
from linebot.models import TextSendMessage
from linebot import (
    LineBotApi, WebhookHandler
)
header = {
    # 用 text/html 方法，以 UTF-8 格式解析
    #'content-type' : 'text/html; charset=UTF-8',
    # 需掛認證資料才可以爬取資料(SuperRich)
    'Authorization' : 'Basic c3VwZXJyaWNoVGg6aFRoY2lycmVwdXM=',
    # 用什麼方式執行(Mozilla、AppleWebKit、Chrome)
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39'
    }

param = {'Language':'TH','Location':'32'}
currency = ['TWD']

def get_exchange_rate(url, name):

  # 使用 requests 套件 get 方法訪問網站
  res = requests.get(url, headers = header)
  # 以下為 json 格式
  if name == 'SuperRich_G' or name == 'Xone' or name == 'SiamExchange' or name == 'SuperRich_O' or name == 'TTExchange':
    # 使用 json 套件，載入 json 格式資料存入 json_rate
    json_rate = json.loads(res.text)
    if name == 'SuperRich_G':
        for i in json_rate['data']['exchangeRate']:
            if str(i['cUnit']) in currency:
                Selling = i['rate'][0]['cSelling']
                Buying = i['rate'][0]['cBuying']
                break
    elif name == 'Xone':
      Selling = json_rate['ExchangeRateGroups'][11]['ExchangeRates'][0]['SellRate']
      Buying = json_rate['ExchangeRateGroups'][11]['ExchangeRates'][0]['BuyRate']
    elif name == 'SiamExchange':
      Selling = json_rate[11]['selling']
      Buying = json_rate[11]['buying']
    elif name == 'SuperRich_O':
        for i in json_rate:
            if i['currencyCode'] in currency:
                Selling = i['sell']
                Buying = i['buy']
                break
    elif name == 'TTExchange':
      for i in json_rate:
        if i['name'][0:3] in currency:
          Selling = i['current_sell_rate']
          Buying = i['current_buy_rate']
          break

  # 以下為 html 格式
  elif name == 'Ratchada' or name == 'GrandSuperRich' or name == 'k79' or name=='Linda' or name == 'P&P' or name == 'vasuexchange' or name == 'twelvevictory':
    # 使用 BeautifulSoup 解析
    soup = BeautifulSoup(res.text, 'html.parser')
    if name == 'Ratchada':
      Selling = soup.find('table',{'class':'tablemembody'}).find('tr',{'id':'TWD'}).find_all('td')[2].text
      Buying = soup.find('table',{'class':'tablemembody'}).find('tr',{'id':'TWD'}).find_all('td')[1].text
    elif name == 'GrandSuperRich':
      count = len(soup.find('table').find_all('tr'))
      for i in range(1,count):
        if soup.find('table').find_all('tr')[i].find_all('td')[2].text[0:3] == 'TWD':
          Selling = soup.find('table').find_all('tr')[i].find_all('td')[4].text
          Buying = soup.find('table').find_all('tr')[i].find_all('td')[3].text
          break

    elif name == 'k79':
      Selling = soup.find_all('tbody')[2].find_all('tr')[16].find_all('td')[4].text
      Buying = soup.find_all('tbody')[2].find_all('tr')[16].find_all('td')[3].text
    elif name == 'Linda':
      Selling = soup.find('tbody').find_all('tr')[25].find_all('td')[3].text
      Buying = soup.find('tbody').find_all('tr')[25].find_all('td')[2].text
    elif name == 'P&P':
      for i in soup.find_all('tr')[1:]:
        if i.find_all('td')[0].text.strip()[0:3] in currency:
          Selling =i.find_all('td')[2].text.strip()
          Buying = i.find_all('td')[1].text.strip()
      # Selling = soup.find_all('tr')[25].find_all('td')[2].text
      # Buying = soup.find_all('tr')[25].find_all('td')[1].text
    elif name == 'vasuexchange':
      Selling = soup.find_all('table',{'bgcolor':'#FFFFFF'})[15].find_all('td')[2].text.strip()
      Buying = soup.find_all('table',{'bgcolor':'#FFFFFF'})[15].find_all('td')[1].text.strip()
    elif name == 'twelvevictory':
      Selling = soup.find('tbody',{'class':'tb-scroll'}).find_all('tr')[8].find_all('td')[3].find('div').find_all('h5')[1].text.strip()
      Buying = soup.find('tbody',{'class':'tb-scroll'}).find_all('tr')[8].find_all('td')[2].find('div').find_all('h5')[1].text.strip()

  # 使用 post 方法， json 格式
  elif name == 'Happyrich':
    res = requests.post(url, headers = header, params = param)
    # 使用 json 套件，載入 json 格式資料存入 json_rate
    json_rate = json.loads(res.text)
    if name == 'Happyrich':
      Selling = json_rate['data'][23]['sellPrice']
      Buying = json_rate['data'][23]['buyPrice']

  return Selling, Buying

def get_exchange_rate_TW(url, name):
    if name == 'MegaBank':
        # 使用 requests 套件 post 方法訪問網站
        res = requests.post(url, headers = header)
        # 使用 json 套件，載入 json 格式資料存入 json_rate
        json_Mega = json.loads(res.text)['appRepBody']['exchangeRates'][10]
        Selling = str(1/float(json_Mega['cashExchangeRate']['buy']))[0:5]
        Buying = str(1/float(json_Mega['cashExchangeRate']['sale']))[0:5]

    elif name == 'TaiwanBank' or name == 'BangkokBank':
        # 使用 requests 套件 get 方法訪問網站
        res = requests.get(url, headers = header)
        res.encoding = 'Big5'
        # 使用 BeautifulSoup 解析
        soup = BeautifulSoup(res.text, 'html.parser')
    if name == 'BangkokBank':
        soup_Bangkok = soup.find_all('tr')[4].find_all('td')
        Selling = str(1/float(soup_Bangkok[0].text))[0:5]
        Buying = str(1/float(soup_Bangkok[1].text))[0:5]
    elif name == 'TaiwanBank':
        soup_TWB = soup.find('table').find('tbody').find_all('tr')[11].find_all('td')
        Selling = str(1/float(soup_TWB[1].text))[0:5]
        Buying = str(1/float(soup_TWB[2].text))[0:5]

    return Selling, Buying

def select_exchange(n=0):
  # 輸入換匯所編號
  # number = 0
  if n == 0:
    print('SuperRich:1, GrandSuperRich:2, Ratchada:3, Xone:4, SiamExchange:5, k79:6')
    number = input('請選擇換匯所')
  else:
    number = n
  # 取得換匯所名稱

  if number == 1:
    name = 'SuperRich_G'
  elif number == 2:
    name = 'SuperRich_O'
  elif number == 3:
    name = 'GrandSuperRich'
  elif number == 4:
    name = 'P&P'
  elif number == 5:
    name = 'SiamExchange'
  elif number == 6:
    name = 'Xone'
  elif number == 7:
    name = 'Linda'
  elif number == 8:
    name = 'Ratchada'
  elif number == 9:
    name = 'vasuexchange'
  elif number == 10:
    name = 'k79'
  elif number == 11:
    name = 'twelvevictory'
  elif number == 12:
    name = 'Happyrich'
  elif number == 13:
    name = 'TTExchange'

  return name

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

# 取得本機 ID & IP
def get_host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return host_name, host_ip
    except:
        print("Unable to get Hostname and IP")

if __name__ == "__main__":
    
    url = [ 'https://www.superrichthailand.com/web/api/v1/rates',
            'https://www.superrich1965.com/controllers/currency.php?method=2&value=33',
            'https://www.grandsuperrich.com/rate_fordemo_v3.php',
            'https://ppmoneyexchage.com/',
            'http://siamexchange.co.th/api/web/index.php?r=v1%2Fcurrency%2Flist',
            'https://x-one.co.th/api/ExchangeRatesContainerApi/',
            'http://www.lindaexchange.com/EN/exchange',
            'http://www.ratchadaexchange.com/',
            'http://www.vasuexchange.com/',
            'https://www.k79exchange.com/',
            'http://www.twelvevictory.com/en/exchange',
            'https://happyrich.co.th/Rate/GetRateService',
            'https://api.software.ttexchange.com/currencies?is_main=false&branch_id=50' ]
    
    url_TW = [ 'http://www.bbl.com.tw/exrate.asp',
               'https://rate.bot.com.tw/xrt/all/day',
               'https://www.megabank.com.tw/api/sc/RateExchange/Get_Fx_Currency']

    name_TW = [ 'BangkokBank', 'TaiwanBank', 'MegaBank']
    
    rate = {'name':[],'sell':[],'buy':[]}
    msg = '\nsell |\tbuy  |\tname\n'

    for i in range(0,len(url)):

        if (i+1==4) or (i+1==5) or (i+1==9): continue
        
        name = select_exchange(i+1)
        
        try:
            sell, buy = get_exchange_rate(url[i], name)
        except:
            continue
    
        rate['name'].append(name)

        if len(str(sell)) != 6:
            if len(str(sell)) == 4:
                sell = str(sell) + '0'
        if len(str(sell)) == 3:
            sell = str(sell) + '00'
        if len(str(buy)) != 6:
            if len(str(buy)) == 4:
                buy = str(buy) + '0'
        if len(str(buy)) == 3:
            buy = str(buy) + '00'

        rate['sell'].append(sell)
        rate['buy'].append(buy)

        msg = msg + str(sell)[0:5] + '|'
        msg = msg + str(buy)[0:5] + '|'
        msg = msg + name + '\n' # [0:11]

    msg = msg + '\n'
    
    for i in range(0,len(name_TW)):
        try:
            sell, buy = get_exchange_rate_TW(url_TW[i], name_TW[i])

            rate['name'].append(name_TW[i])
            rate['sell'].append(sell)
            rate['buy'].append(buy)

            msg = msg + str(sell)[0:5] + '|'
            msg = msg + str(buy)[0:5] + '|'
            msg = msg + name_TW[i] + '\n' # [0:11]
        except:
            continue

    # 取得本機 ID & IP
    host_name, host_ip = get_host_name_IP()

    # 取得現在時間
    time_now = time.strftime('%Y-%m-%d %I:%M:%S %p',time.localtime())

    token = [os.getenv('LINE_USER_ID'), os.getenv('LINE_GROUP_ID')]
    
    # USER
    LineNotify(os.getenv('LINE_USER_ID'), '\n' + time_now + '\n'+ msg + '\n' + "Hostname :  " + host_name + '\n' + "IP :  " + host_ip)
    
    # GOUPR
    LineNotify(os.getenv('LINE_GROUP_ID'), msg + '\n各換匯所資料更新依官方為準\n以上提供資訊僅供參考，仍依現場標示匯率為準')
    
