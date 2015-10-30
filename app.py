import tornado.ioloop
import tornado.web
import settings
import urls

if __name__ == '__main__':
    application = tornado.web.Application(urls.urls, **settings.settings)
    application.listen(8866)
    tornado.ioloop.IOLoop.current().start()
