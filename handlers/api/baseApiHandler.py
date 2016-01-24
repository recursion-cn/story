#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/12/04

import tornado.web
from handlers import baseHandler
from modules.db import db
import constants

class RequestHandler(baseHandler.RequestHandler):

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