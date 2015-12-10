#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/12/10

from modules.db import db

"""
Member class
"""
class Member:

    def __init__(self, nick, password, created, updated=None, id=None):
        self.id = id
        self.nick = nick
        self.password = password
        self.created = created
        self.updated = updated

    def add(self):
        pass

    @classmethod
    def getByNick(cls, nick):
        query = 'select id, nick, password, created, updated from tb_user where nick = %s'
        member = db.get(query, nick)
        return member

    @classmethod
    def getById(cls, id):
        query = 'select id, nick, password, created, updated from tb_user where id = %s'
        member = db.get(query, id)
        return member

    def updateNick(self, new_nick):
        if self.id:
            update = 'update tb_user set nick = %s where id = %s'
            row = db.update(update, new_nick, self.id)
            return row
        return 0

    def updatePassword(self, new_password):
        if self.id:
            update = 'update tb_user set password = %s where id = %s'
            row = db.update(update, new_password, self.id)
            return row
        return 0