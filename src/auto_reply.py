# coding=utf8
"""
main script using itchat to communicate with WeChat and send tuling123 response (AI text processing) back

TODO: currently single thread POC, future will replace requests with threading or asyncio (aiohttp)
"""

import logging
import requests
import itchat



def get_response(message, url='http://www.tuling123.com/openapi/api', userid='Gerald', key='ba635c693fd745828b5a49cc7f5d3be5'):
    """send message to remote sever
    url = url for remote server
    key = API key
    return json {"text": String, "code": integer}
    """

    data = {'key':key, 'info':message, 'userid':userid}
    result = requests.post(url, data=data)
    return result.json()

@itchat.msg_register(itchat.content.TEXT)
def chat_reply(message):
    """itchat (callback) will use it to process messages
    this function is used for peer to peer chat
    """

    try:
        reply = get_response(message['Text'])
        if reply['code'] == 1000:
            return reply
    except requests.exceptions.RequestException as error:
        logging.error(error)
        logging.error(reply)
    return 'I received: ' + message['Text']

@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_chat__reply(message):
    """itchat (callback) will use it to process messages
    this function is used for group chat
    """
    if not 'isAt' in message:
        return
    try:
        reply = get_response(message['Text'])
        if reply['code'] == 1000:
            itchat.send(u'@%s\u2005: %s' % (message['ActualNickName'], reply), message['FromUserName'])
    except requests.exceptions.RequestException as error:
        logging.error(error)
        logging.error(reply)

def main():
    """entry point
    """

    itchat.auto_login(hotReload=True)
    itchat.run()
if __name__ == '__main__':
    main()
