#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/12/15

from modules.db import db
import datetime, time

class Post:

    tb_name = 'tb_post'

    def __init__(self):
        pass

    @classmethod
    def count_posts(cls, user_id):
        return Post.__count(Post.tb_name, user_id=user_id)

    @classmethod
    def count_posts_by_category(cls, user_id, category_id):
        return Post.__count(Post.tb_name, user_id=user_id, category_id=category_id)

    @classmethod
    def count_drafts(cls, user_id):
        return Post.__count(Post.tb_name, 0, user_id=user_id)

    @classmethod
    def count_drafts_by_category(cls, user_id, category_id):
        return Post.__count(Post.tb_name, 0, user_id=user_id, category_id=category_id)

    @classmethod
    def list(cls, user_id, offset=0, size=10):
        return Post.__list(Post.tb_name, user_id=user_id, offset=offset, size=size)

    @classmethod
    def drafts(cls, user_id, offset=0, size=10):
        return Post.__list(Post.tb_name, 0, user_id=user_id, offset=offset, size=size)

    @classmethod
    def drafts_by_category(cls, user_id, category_id, offset=0, size=10):
        return Post.__list(Post.tb_name, 0, user_id=user_id, category_id=category_id, offset=offset, size=size)

    @classmethod
    def list_by_category(cls, user_id, category_id, offset=0, size=10):
        return Post.__list(Post.tb_name, user_id=user_id, category_id=category_id, offset=offset, size=size)

    @classmethod
    def get_post(cls, id):
        return Post.__get_post(Post.tb_name, id)

    @classmethod
    def pretend_delete(cls, id):
        delete = 'update tb_post set deleted = 1 where id = %s'
        row = db.update(delete, id)
        return row > 0

    @staticmethod
    def __count(table_name, visible=1, deleted=0, user_id=None, category_id=None):
        count_sql = 'select count(1) count from {0} where visible = %s and deleted = %s '.format(table_name)
        if user_id and category_id:
            count_sql += 'and user_id = %s and category_id = %s'
            count_res = db.get(count_sql, visible, deleted, user_id, category_id)
            return count_res.count
        elif user_id:
            count_sql += 'and user_id = %s'
            count_res = db.get(count_sql, visible, deleted, user_id)
            return count_res.count
        elif category_id:
            count_sql += 'and category_id = %s'
            count_res = db.get(count_sql, visible, deleted, category_id)
            return count_res.count
        else:
            count_res = db.get(count_sql, visible, deleted)
            return count_res.count

    @staticmethod
    def __list(table_name, visible=1, deleted=0, user_id=None, category_id=None, offset=0, size=10):
        list_sql = """
                    select id, title, content, user_id, category_id, public, visible,
                    if(updated is NULL, created, updated) last_modified from {0}
                    where visible = %s and deleted = %s """.format(table_name)
        list = None
        if user_id and category_id:
            list_sql += 'and user_id = %s and category_id = %s order by last_modified desc limit %s, %s'
            list = db.query(list_sql, visible, deleted, user_id, category_id, offset, size)
        elif user_id:
            list_sql += 'and user_id = %s order by last_modified desc limit %s, %s'
            list = db.query(list_sql, visible, deleted, user_id, offset, size)
        elif category_id:
            list_sql += 'and category_id = %s order by last_modified desc limit %s, %s'
            list = db.query(list_sql, visible, deleted, category_id, offset, size)
        else:
            list_sql += 'order by last_modified desc limit %s, %s'
            list = db.query(list_sql, visible, deleted, offset, size)
        if list:
            for post in list:
                post['last_modified'] = time.mktime(post.last_modified.timetuple())

        return list

    @staticmethod
    def __get_post(table_name, id=None, title=None):
        get_sql = """
                    select id, title, content, user_id, category_id, public, visible,
                    if(updated is NULL, created, updated) last_modified from {0}
                    where deleted = 0 """.format(table_name)
        post = None
        if id:
            get_sql += 'and id = %s'
            post = db.get(get_sql, id)
        if title:
            get_sql += 'and title = %s'
            post = db.get(get_sql, title)
        if post:
            post['last_modified'] = time.mktime(post.last_modified.timetuple())
        return post
