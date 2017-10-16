#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
tuling is script that talks to tuling123.com for AI response

"""

import logging
import threading
import time
import requests

class Tuling(threading.Thread):
    """Tuling AI thread
    """

    def __init__(self, queue_in, queue_out, **kwargs):
        #url=None, userid=None, key=None):
        """
        queue_in: Queue.Queue() object for incomming message (need AI process)
        queue_out: Queue.Queue() object for outgoing message (processed by AI)
        **kwargs:
            url: tuling url
            userid: tuling userid
            key: tuling API key
        """

        self.queue_in = queue_in
        self.queue_out = queue_out
        self._payload_ = {
            'url': 'http://www.tuling123.com/openapi/api',
            'userid': 'Gerald',
            'key': 'ba635c693fd745828b5a49cc7f5d3be5'}
        for key in kwargs:
            if key in self._payload_:
                self._payload_[key] = kwargs[key]
        self._stop_ = False
        super(Tuling, self).__init__()

    def stop(self):
        """
        stop thread while loop. thread will end
        """

        self._stop_ = True

    def run(self):
        """thread entry point
        """

        while True:
            if not self.queue_in.empty():
                try:
                    response = requests.post(
                        self._payload_['url'], data={
                            'key': self._payload_['key'],
                            'info': self.queue_in.get(),
                            'userid': self._payload_['userid']}).json()
                    if response['code'] == 100000:
                        self.queue_out.put(response['text'])
                        raise ValueError(response)
                except Exception as error:
                    logging.error(error, exc_info=True)
                    logging.error("error get response from AI backend and put to output queue")
            time.sleep(0.1)
            if self._stop_:
                break
