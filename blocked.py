from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection

class handler(SockJSConnection):
    def on_message(self, msg):
        h = {}
        print("Received: %s" % msg)
        print("Entering blocked loop.")
        #for i in range(0,10000000):
        for i in range(0,1000000):
            h[i] = i
            i = h.get(i)
            h[i] = i - 1
            i = h.get(i)
            h[i] = i + 1
        print("Done blocking.")
        self.send('done')

if __name__ == '__main__':
    print("Starting up.")
    router = SockJSRouter(handler, '/push')

    print("Registering router: %s" % router.urls)
    app = web.Application(router.urls)

    app.listen(8080)
    print("Starting IOLoop.")
    ioloop.IOLoop.instance().start()
    print("Done.")
