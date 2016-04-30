from tornado import web, ioloop, httpclient, gen, process
from sockjs.tornado import SockJSRouter, SockJSConnection

from multiplex import MultiplexConnection
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

executor = ThreadPoolExecutor(4)
process = ProcessPoolExecutor()

def handler(conn):
    future = process.submit(blocking_io)
    future.result()
    conn.send("done")
    return "done"

def blocking_io():
    h = {}
    for i in range(0,5000000):
        h[i] = i
        i = h.get(i)
        h[i] = i - 1
        i = h.get(i)
        h[i] = i + 1
    return "done"


class Connection(SockJSConnection):
    def on_message(self, msg):
        print("Received: %s" % msg)
        executor.submit(handler, self)

if __name__ == '__main__':
    print("Starting up.")
    router = SockJSRouter( Connection, '/push' )
    app = web.Application(router.urls)
    app.listen(8080)

    print("Starting IOLoop.")
    ioloop.IOLoop.instance().start()
    print("Done.")
