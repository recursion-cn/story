#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
from modules.db import db
import constants
from concurrent.futures import ThreadPoolExecutor
import tornado.ioloop

class RequestHandler(tornado.web.RequestHandler):

    #executor = ThreadPoolExecutor(3)
    #io_loop = tornado.ioloop.IOLoop.current()

    def initialize(self):
        user_agent = self.request.headers.get('User-Agent')
        if user_agent:
            user_agent = user_agent.lower()
            if user_agent.find('iphone') > -1 or user_agent.find('android') > -1:
                self.is_mobile = True
            else:
                self.is_mobile = False

    def get(self):
        raise tornado.web.HTTPError(404)

    def get_current_user(self):
        cookie = self.get_secure_cookie('current_user')
        if cookie:
            current_user = {}
            array = cookie.split('&')
            for i in range(len(array)):
                pair = array[i].split('=')
                current_user[pair[0]] = pair[1]
            return current_user
        return None

    def write_error(self, status_code, **kwargs):
        if status_code == 403:
            self.render('403.html')
        elif status_code == 404:
            self.render('404.html')
        elif status_code == 500:
            self.render('500.html')
        else:
            super(RequestHandler, self).write_error(status_code, **kwargs)

    def send_result(self, success=False, data=None, error_code=constants.error_code['internal_error'], msg=None):
        default_res = dict(
            success = success,
            data = data,
            error_code = error_code,
            msg = msg
        )
        self.write(default_res)
        self.finish()
