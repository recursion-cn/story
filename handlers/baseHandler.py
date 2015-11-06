#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
from modules.db import db

class RequestHandler(tornado.web.RequestHandler):

    def get(self):
        raise tornado.web.HTTPError(404)

    def get_current_user(self):
        current_nick = self.get_secure_cookie('current_user')
        current_user = None
        if current_nick:
            query = 'select id, nick from tb_user where nick = %s'
            current_user = db.get(query, current_nick)

        return current_user

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        elif status_code == 500:
            self.render('500.html')
        else:
            super(RequestHandler, self).write_error(status_code, **kwargs)
