#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/10/28

import baseHandler
from modules.db import db

"""
get the records list
@return records list
"""
class ListHandler(baseHandler.RequestHandler):

    def get(self):
        query = 'select id, title, content, created, updated from tb_post where visible = 1'
        records = db.query(query)

        self.render('index.html', records=records)

"""
direct to the edit page 
"""
class EditHandler(baseHandler.RequestHandler):
    
    def get(self):
        self.render('edit.html')
