#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/12/03

import baseApiHandler
from modules.db import db
import modules.utils
import datetime
import tornado.web
from settings import settings
import json
import constants

"""
add like interaction on a post
"""
class LikeHandler(baseApiHandler.RequestHandler):
    def post(self):
        post_id = self.get_body_argument('post_id', None)
        print post_id
        if post_id:
            has_liked = self.get_cookie('like')
            if not has_liked:
                now = datetime.datetime.now()
                if self.current_user:
                    has_user_liked = 'select count(1) count from tb_interaction where user_id = %s and post_id = %s'
                    liked_count = db.get(has_user_liked, self.current_user.id, post_id)
                    if not liked_count.count:
                        add_like = 'insert into tb_interaction (user_id, post_id, `like`, unlike, created) values (%s, %s, %s, %s, %s)'
                        like_id = db.insert(add_like, self.current_user.id, post_id, '1', '0', now)
                        if like_id:
                            self.write({'success': True})
                            self.finish()
                            return
                else:
                    add_like = 'insert into tb_interaction (post_id, `like`, unlike, created) values (%s, %s, %s, %s)'
                    like_id = db.insert(add_like, post_id, 1, 0, now)
                    if like_id:
                        self.write({'success': True})
                        self.finish()