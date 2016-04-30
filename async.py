from tornado import web, ioloop, httpclient, gen
from sockjs.tornado import SockJSRouter, SockJSConnection

from multiplex import MultiplexConnection
from concurrent.futures import ThreadPoolExecutor

def blocking_io():
    h = {}
    for i in range(0,10000000):
        h[i] = i
        i = h.get(i)
        h[i] = i - 1
        i = h.get(i)
        h[i] = i + 1
    return "done"


class Connection(SockJSConnection):
    @web.asynchronous
    def on_message(self, msg):
        print("Received: %s" % msg)
        print("Async.")
        response = yield blocking_io()
        print("Done blocking.")
        self.send(response)

if __name__ == '__main__':
    print("Starting up.")
    router = SockJSRouter( Connection, '/push' )
    app = web.Application(router.urls)
    app.listen(8080)
    print("Starting IOLoop.")
    ioloop.IOLoop.instance().start()
    print("Done.")
