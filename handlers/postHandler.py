#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/10/28

import baseHandler
from modules.db import db
import datetime
import markdown
from bs4 import BeautifulSoup
import tornado.web

"""
get the posts list
@return posts list
"""
class ListHandler(baseHandler.RequestHandler):

    def get(self):
        query = 'select id, title, content, user_id, category_id, created, updated from tb_post where visible = 1 order by if(updated is NULL, created, updated) desc'
        posts = db.query(query)
        users_id = []
        if posts:
            for post in posts:
                _html = markdown.markdown(post.content)
                soup = BeautifulSoup(_html, 'html.parser')
                _text = soup.get_text()
                if not post['user_id'] in users_id:
                    users_id.append(str(post['user_id']))
                if _text and len(_text) > 200:
                    _text = _text[0:200] + '...'
                post['summary'] = _text
                post['last_modified'] = post['updated'] if post['updated'] else post['created']
            select_uses = 'select id, nick from tb_user where id in (' + ','.join(users_id) + ')'
            users = db.query(select_uses)
            for post in posts:
                for user in users:
                    if post['user_id'] == user['id']:
                        post['author'] = user

        self.render('index.html', posts=posts, draft=False)

"""
get user's drafts
"""
class DraftListHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        query = 'select id, title, content, user_id, created, updated from tb_post where user_id = %s and visible = 0 order by if(updated is NULL, created, updated) desc'
        drafts = db.query(query, self.current_user.id)
        for draft in drafts:
            draft['author'] = self.current_user
            draft['last_modified'] = draft['updated'] if draft['updated'] else draft['created']
            _html = markdown.markdown(draft.content)
            soup = BeautifulSoup(_html, 'html.parser')
            _text = soup.get_text()
            if _text and len(_text) > 200:
                _text = _text[0:200] + '...'
            draft['summary'] = _text

        self.render('index.html', posts=drafts, draft=True)

"""
get single post by id
"""
class PostHandler(baseHandler.RequestHandler):

    def get(self, id):
        query = 'select id, title, content, user_id, visible, created, updated from tb_post where id = %s'
        post = db.get(query, id)
        query_author = 'select id, nick from tb_user where id = %s'
        author = db.get(query_author, post.user_id)
        post['author'] = author

        self.render('post.html', post=post)

"""
direct to the edit page
"""
class EditHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self, post_id=None):
        if post_id:
            get_post = 'select id, title, content, category_id from tb_post where id = %s'
            post = db.get(get_post, post_id)
        get_categories = 'select id, name from tb_category where visible = 1'
        categories = db.query(get_categories)

        self.render('edit.html', categories=categories, post=post)

"""
create new post
"""
class NewHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def post(self, user_id=1):
        title = self.get_body_argument('title')
        content = self.get_body_argument('content')
        category_id = self.get_body_argument('category')
        visible = 1 - int(self.get_body_argument('draft'))

        if title and content and category_id:
            sql = 'insert into tb_post (title, content, user_id, category_id, visible, created) values (%s, %s, %s, %s, %s, %s)'
            now = datetime.datetime.now()
            post_id = db.insert(sql, title, content, long(user_id), int(category_id), int(visible), now)
            if post_id:
                self.write({'success': True})
                self.finish()
                return
            self.write({'success': False})
            self.finish()
            return
        self.write({'success': False})
        self.finish()
