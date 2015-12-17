#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/12/04

import tornado.web
from modules.db import db
import constants

class RequestHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        current_nick = self.get_secure_cookie('current_user')
        current_user = None
        if current_nick:
            query = 'select id, nick from tb_user where nick = %s'
            current_user = db.get(query, current_nick)

        return current_user

    def send_result(self, success=False, data=None, error_code=constants.error_code['internal_error'], msg=None):
        default_res = dict(
            success = success,
            data = data,
            error_code = error_code,
            msg = msg
        )
        self.write(default_res)
        self.finish()

    def send_success(self, data):
        self.send_result(True, data, error_code=None)

    def send_error(self, error_code, msg=None):
        self.send_result(error_code=error_code, msg=msg)