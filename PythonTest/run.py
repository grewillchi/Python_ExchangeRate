import requests
from linebot.models import TextSendMessage
from linebot import (
    LineBotApi, WebhookHandler
)

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

token = 'LINE_USER_ID'
msg = 5*3

if __name__ == "__main__":
    LineNotify(token, msg)
