# coding=utf8
import requests
import itchat

KEY = 'ba635c693fd745828b5a49cc7f5d3be5'


def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'

    data = {
        'key': KEY,
        'info': msg,
        'userid': 'Gerald'
    }

    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    default_reply = 'I received: ' + msg['Text']
    reply = get_response(msg['Text'])
    return reply or default_reply


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        reply = get_response(msg['Text'])
        itchat.send(u'@%s\u2005: %s' % (msg['ActualNickName'], reply), msg['FromUserName'])

itchat.auto_login(hotReload=True)
itchat.run()

