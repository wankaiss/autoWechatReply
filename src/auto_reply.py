# coding=utf8
"""
WeChat main script
"""
import Queue
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from src.wechat import WechatBot
from src.tuling import Tuling

QUEUE_QR = Queue.Queue()


class myHandler(BaseHTTPRequestHandler):
    """customer handler for BaseHTTPServer
    """

    def __init__(self, ip, port, handler):
        BaseHTTPRequestHandler.__init__(self, ip, port, handler)

    def do_GET(self):
        """handle HTTP GET request
        """

        if self.path == '/login':
            try:
                qr_code = QUEUE_QR.get(timeout=30)
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(qr_code)
            except Queue.Empty as _:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('where is my QR code?')
        if self.path == '/logout':
            # TODO: need to add handler for logout. Need to figure out matching accounts
            pass


def main(host='', port_number=80):
    """entry point
    """
    queue_wechat_in = Queue.Queue()
    queue_wechat_out = Queue.Queue()

    # FIXME: just try 10 threads. need more for wechat_instances and recycle/restart unused.
    # seems ItChat use this per account
    wechat_instances = []
    for instance in range(10):
        wechat_instances.append(WechatBot(queue_wechat_in, queue_wechat_out, QUEUE_QR))
        wechat_instances[instance].start()

    # FIXME: the tuling instance can shared by all users
    tuling_instances = []
    for instance in range(10):
        tuling_instances.append(Tuling(queue_wechat_out, queue_wechat_in))
        tuling_instances[instance].start()

    try:
        server = HTTPServer((host, port_number), myHandler)
        server.serve_forever()
    except Exception as _:
        server.socket.close()

if __name__ == '__main__':
    main()
