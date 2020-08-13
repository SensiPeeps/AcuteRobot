import os, tornado
from acutebot.helpers.spthelper import urls

PORT = os.environ.get("PORT", 8888)

def start():

    print("Tornado server started")

    app = tornado.web.Application(urls)
    app.listen(PORT, address='0.0.0.0')
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
   start()
