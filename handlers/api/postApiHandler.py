#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/12/03

import baseApiHandler
from modules.db import db
from models.Post import Post
import modules.utils
import datetime
import tornado.web
from settings import settings
import json
import constants

"""
get single post by id
"""
class PostHandler(baseApiHandler.RequestHandler):

    def get(self, id):
        post = Post.get_post(id)
        if post:
            if not ord(post.public):
                if not self.current_user:
                     self.write_error(403, '您没有该文章的阅读权限')
                     return
                elif self.current_user.id != post.user_id:
                    self.write_error(403, '您没有该文章的阅读权限')
                    return
            query_author = 'select id, nick from tb_user where id = %s'
            author = db.get(query_author, post.user_id)
            post['author'] = author
            post = json.dumps(post, cls=modules.utils.JSONEncoder)
            self.write({'success': True, 'post': post})
            self.finish()
            return

        self.write_error(404)

"""
add like interaction on a post
"""
class LikeHandler(baseApiHandler.RequestHandler):
    def post(self):
        post_id = self.get_body_argument('post_id', None)
        if post_id:
            has_liked = self.get_cookie('like')
            if not has_liked:
                now = datetime.datetime.now()
                if self.current_user:
                    has_user_liked = 'select count(1) count from tb_interaction where user_id = %s and post_id = %s'
                    liked_count = db.get(has_user_liked, self.current_user.id, int(post_id))
                    if not liked_count.count:
                        add_like = 'insert into tb_interaction (user_id, post_id, `like`, unlike, created) values (%s, %s, %s, %s, %s)'
                        like_id = db.insert(add_like, self.current_user.id, post_id, 1, 0, now)
                        if like_id:
                            #self.set_cookie('like_post_{0}'.format(post_id), '1', expires_days=999)
                            self.write({'success': True})
                            self.finish()
                            return
                else:
                    add_like = 'insert into tb_interaction (post_id, `like`, unlike, created) values (%s, %s, %s, %s)'
                    like_id = db.insert(add_like, post_id, 1, 0, now)
                    if like_id:
                        #self.set_cookie('like_post_{0}'.format(post_id), '1', expires_days=999)
                        self.write({'success': True})
                        self.finish()
