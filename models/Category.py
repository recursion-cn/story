#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/12/15

from modules.db import db

class Category:
    def __init__(self):
        pass

    @classmethod
    def list(cls, user_id):
        query_list = 'select id, name from tb_category where user_id = %s'
        categories = db.query(query_list, user_id)
        return categories

    @classmethod
    def get(cls, category_id):
        get_one = 'select id, name from tb_category where nick = %s'
        category = db.get(get_one)
        return category