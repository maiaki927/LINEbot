from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import os

import requests



app = Flask(__name__)
#請在左方.env的檔案中加上： SECRET ='這裡面請填你line後台的SECRET碼' 
line_SECRET=os.environ.get('SECRET')

#或是將line_SECRET直接代入line後台的SECRET碼 但不建議 因是公開的會被他人看到
#line_SECRET = 'line後台的SECRET碼'

# Channel Access Token
line_bot_api = LineBotApi('這裡請填入line後台的Channel Access Token')
# Channel Secret           
handler = WebhookHandler(line_SECRET)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        
        handler.handle(body, signature)    
    except InvalidSignatureError:
        abort(100)
    return 'OK'

# 處理訊息 
#以下這段請先將LINE後台的webhook認證成功後 再將這段取消註解
'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    message = TextSendMessage(text=event.message.text)
   
    line_bot_api.reply_message(event.reply_token, message)
'''  
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
