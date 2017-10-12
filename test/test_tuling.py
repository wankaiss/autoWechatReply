#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""test src/tuling.py
"""
import Queue
from src.tuling import Tuling
import responses

@responses.activate
def test_Tuling():
    """test Tuling server
    """
    queue_in = Queue.Queue()
    queue_out = Queue.Queue()
    with responses.RequestsMock() as resp:
        resp.add(responses.POST,
                'http://www.tuling123.com/openapi/api',
                json={'text':'hello client', 'code':100000})
        ai_server = Tuling(queue_in, queue_out, key='test')
        assert ai_server._payload_['key'] == 'test'
        try:
            ai_server.start()
            queue_in.put('hello server')
            message = queue_out.get(timeout=5)
        finally:
            ai_server.stop()
            ai_server.join()
        assert message == 'hello client'
