#!/usr/bin/env python3

from tornado.web import Application, RequestHandler
from tornado import httpserver, ioloop
import subprocess


class Handler(RequestHandler):
    def get(self):
        print(self.request.path)
        if(self.request.path == '/shutdown/'):
            self.write('shutting down...')
            self.flush()
            results = subprocess.check_output(['shutdown', '-h',
                'now'])
        else:
            self.set_status(403)
            self.write('unknow path')
        self.finish()


if __name__ == '__main__':
    import sys
    app = Application([(r'/shutdown/', Handler), ])
    server = httpserver.HTTPServer(app)
    if(len(sys.argv) == 2):
        # listen port specified
        server.listen(sys.argv[1], address='0.0.0.0')
    else:
        server.listen(8888, address='0.0.0.0')
    ioloop.IOLoop.current().start()
