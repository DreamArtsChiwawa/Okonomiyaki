import os
import json
import requests
from flask import Flask, request

import analyze
import preprocess

app = Flask(__name__)
env = os.environ


@app.route('/', methods=['GET'])
def helloPage():
    return "Hello python bot."


@app.route('/messages', methods=['POST'])

def messages():
    if is_request_valid(request):

        body = request.get_json(silent=True)

        companyId = body['companyId']
        msgObj = body['message']
        groupId = msgObj['groupId']
        messageText = msgObj['text']
        userName = msgObj['createdUserName']

        flag = 0
        
        if messageText.find('週報') and messageText.find('判断')　== 1:
            send_message(companyId, "判断したい週報を入力してください！")
            flag = 1
            
        if messageText.find('<< WEEKLY REPORT >>') == 1:
            preprocessed_text = preprocess.preprocess(messageText) #テキストをAIに読みやすいようにする工程

            
        if flag == 0:
            value = analyze.analyze(preprocessed_text)
            #value = dammy() #ダミーの辞書を生成 
            return_message, return_message2, return_message3 = set_message(value) #メッセージを整形

            send_message(companyId, groupId, return_message) #メッセージを送信
            send_message(companyId, groupId, return_message2)
            send_message(companyId, groupId, return_message3)
        

        print("MESSEAGES SENDED") #log

        return "OK"

    else:

        return "Request is not valid."


# Check if token is valid.
def is_request_valid(request):
    validationToken = env['CHIWAWA_VALIDATION_TOKEN']

    requestToken = request.headers['X-Chiwawa-Webhook-Token']

    return validationToken == requestToken


# Send message to Chiwawa server
def send_message(companyId, groupId, message):
    url = 'https://{0}.chiwawa.one/api/public/v1/groups/{1}/messages'.format(companyId, groupId)

    headers = {

        'Content-Type': 'application/json',

        'X-Chiwawa-API-Token': env['CHIWAWA_API_TOKEN']

    }

    content = {

        'text': message

    }

    requests.post(url, headers=headers, data=json.dumps(content))


def set_message(analyzed_value):
    message = "とってもポジティブな文章は、\n「" + analyzed_value['max']['sentence'] + \
                "」\nで、" + str(analyzed_value['max']['score']) + "点でした！\n"
                
                
    message2 = "すっごくネガティブな文章は、\n「" + analyzed_value['min']['sentence'] + \
                "」\nで、" + str(analyzed_value['min']['score']) + "点でした><\n"
       
    message3 =  "ウィークリーレポートの総計は、" + str(analyzed_value['total']) + "点でした\n" \
                "来週もがんばりましょう！！"
        
    """
    message = 'RESULT' + \
              '\nMAX = ' + str(analyzed_value['max']['score']) + \
              '\nMIN = ' + str(analyzed_value['min']['score']) + \
              '\nMID = ' + str(analyzed_value['mid']['score']) + \
              '\nMAGNITUDE = ' + str(analyzed_value['magnitude']) + \
              '\nTOTAL = ' + str(analyzed_value['total'])
    """
    return message,message2,message3
"""
def dammy():
    dic = {'max': {'score': 0.8, 'sentense':"あｆｐふぁｗｋぱ"},
           'min': {'score': -0.4,'sentense':"うぃふぉあえふぉうぇ"},
           'sum': 14,
           'ave': -0.5,
           'mid': {'score': 0},
           'magnitude': 11,
           'total': -4}
    
    return dic
"""

if __name__ == '__main__':
    app.run(host='', port=80, debug=True)