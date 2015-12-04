#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/12/04

import tornado.web
from modules.db import db

class RequestHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        current_nick = self.get_secure_cookie('current_user')
        current_user = None
        if current_nick:
            query = 'select id, nick from tb_user where nick = %s'
            current_user = db.get(query, current_nick)

        return current_user