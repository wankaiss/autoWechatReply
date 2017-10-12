# coding=utf8
"""
WeChat bot by using ItChat
"""

import logging
import threading
import Queue
import itchat

class WechatBot(threading.Thread):
    """WechatBot
    """

    def __init__(self, queue_in, queue_out, queue_qr):
        """
        queue_in: Queue.Queue() object for receive message returned by AI
        queue_out: Queue.Queue() object for send message for AI to process
        queue_qr: Queue.Queue() object for send qr_code
        """

        self.queue_in = queue_in
        self.queue_out = queue_out
        self.queue_qr = queue_qr
        self._timeout_ = 30
        super(WechatBot, self).__init__()

    @itchat.msg_register(itchat.content.TEXT)
    def chat_reply(self, message):
        """itchat (callback) to process peer to peer chat
        """

        self.queue_out(message['Text'])
        try:
            reply = self.queue_in.get(timeout=self._timeout_)
        except Queue.Empty as _:
            logging.error("reach max timeout of %s on self.queue_in on peer to peer callback", self._timeout_)
            reply = 'I received: {}'.format(message['Text'])
        return reply

    @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
    def group_chat__reply(self, message):
        """itchat (callback) to process group chat
        """

        if not 'isAt' in message:
            return
        self.queue_out(message['Text'])
        try:
            reply = self.queue_in.get(timeout=self._timeout_)
            itchat.send(u'@%s\u2005: %s' % (message['ActualNickName'], reply), message['FromUserName'])
        except Queue.Empty as _:
            logging.error("reach max timeout of %s on self.queue_in on group chat callback", self._timeout_)

    def callback(self, uuid, status, qrcode):
        """put QR code queue
        """

        logging.info(uuid, status)
        self.queue_qr.put(qrcode)

    def run(self):
        """thread entry point
        """

        try:
            itchat.auto_login(hotReload=True, qrCallback=self.callback)
            itchat.run()
        finally:
            itchat.logout()
