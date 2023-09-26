import requests
import os
import json
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

def get_exchange_rate(url, name):

  # 使用 requests 套件 get 方法訪問網站
  res = requests.get(url, headers = header)
  # 以下為 json 格式
  if name == 'SuperRich_G' or name == 'Xone' or name == 'SiamExchange' or name == 'SuperRich_O':
    # 使用 json 套件，載入 json 格式資料存入 json_rate
    json_rate = json.loads(res.text)
    if name == 'SuperRich_G':
      Selling = json_rate['data']['exchangeRate'][13]['rate'][0]['cSelling']
      Buying = json_rate['data']['exchangeRate'][13]['rate'][0]['cBuying']
    elif name == 'Xone':
      Selling = json_rate['ExchangeRateGroups'][11]['ExchangeRates'][0]['SellRate']
      Buying = json_rate['ExchangeRateGroups'][11]['ExchangeRates'][0]['BuyRate']
    elif name == 'SiamExchange':
      Selling = json_rate[11]['selling']
      Buying = json_rate[11]['buying']
    elif name == 'SuperRich_O':
      Selling = json_rate[13]['sell']
      Buying = json_rate[13]['buy']

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
      Selling = soup.find('tbody',{'class':'tb-scroll'}).find_all('tr')[8].find_all('td')[3].find('div').find('h5').text.strip()
      Buying = soup.find('tbody',{'class':'tb-scroll'}).find_all('tr')[8].find_all('td')[2].find('div').find('h5').text.strip()

  # 使用 post 方法， json 格式
  elif name == 'Happyrich':
    res = requests.post(url, headers = header, params = param)
    # 使用 json 套件，載入 json 格式資料存入 json_rate
    json_rate = json.loads(res.text)
    if name == 'Happyrich':
      Selling = json_rate['data'][23]['sellPrice']
      Buying = json_rate['data'][23]['buyPrice']

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

if __name__ == "__main__":
    
    token = os.getenv('LINE_USER_ID')
    url = 'https://www.superrichthailand.com/web/api/v1/rates'

    rate = {'name':[],'sell':[],'buy':[]}
    msg = '\nsell |\tbuy  |\tname\n'

    name = select_exchange(1)
    # msg = 5*3

    sell, buy = get_exchange_rate(url, name)
        
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

    msg = msg + str(sell).ljust(5) + '|'
    msg = msg + str(buy).ljust(5) + '|'
    msg = msg + name[0:11] + '\n'

    LineNotify(token, msg)
