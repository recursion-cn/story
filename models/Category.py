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
    def list(owner_nick):
        query_list = 'select id, name from tb_category where nick = %s'
        categories = db.query(query_list, nick)
        return categories

    @classmethod
    def get(category_id):
        get_one = 'select id, name from tb_category where nick = %s'
        category = db.get(get_one)
        return category