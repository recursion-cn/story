#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/12/15

from modules.db import db

class Post:

    def __init__(self):
        pass

    @classmethod
    def count_posts(cls, user_id):
        get_count = 'select count(1) count from tb_post where visible = 1 and deleted = 0 and user_id = %s'
        count_row = db.get(get_count, user_id)
        if count_row:
            return count_row.count

    @classmethod
    def list(cls, user_id, offset=0, size=10):
        query_list = """select id, title, content, category_id, created, updated, if(updated is NULL, created, updated) last_modified 
                        from tb_post where visible = 1 and deleted = 0 and user_id = %s order by last_modified desc limit %s, %s"""
        posts = db.query(query_list, user_id, offset, size)
        return posts

    @classmethod
    def drafts(cls, user_id, offset=0, size=10):
        query_drafts = """select id, title, content, category_id, created, updated, if(updated is NULL, created, updated) last_modified 
                          from tb_post where visible = 0 and deleted = 0 and user_id = %s order by last_modified desc limit %s, %s"""
        drafts = db.query(query_drafts, user_id, offset, size)
        return drafts

    @classmethod
    def get_post(cls, id):
        get_post = """select id, title, content, user_id, category_id, public, visible, if(updated is NULL, created, updated) last_modified 
                      from tb_post where id = %s and deleted = 0"""
        post = db.get(get_post, id)
        return post

    @classmethod
    def pretend_delete(cls, id):
        delete = 'update tb_post set deleted = 1 where id = %s'
        row = db.update(delete, id)
        return row > 0