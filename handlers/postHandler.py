#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/10/28

import baseHandler
from modules.db import db
import modules.utils
import datetime
import markdown
import bleach
from bs4 import BeautifulSoup
import tornado.web
from settings import settings
import json

"""
get the public posts list
"""

class PublicListHandler(baseHandler.RequestHandler):

    def get(self):
        query = """select id, title, content, user_id, category_id, created, updated, from tb_post
                 where public = 1 and visible = 1 and deleted = 0 order by if(updated is NULL, created, updated) desc
                 limit 0, 20
                """
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

        self.render('index.html', posts=posts)

"""
get the current user's posts list, need login.
@return posts list
"""
class ListHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        size = 10
        needPagination = False
        args = self.request.arguments
        if args.get('size'):
            size = int(args.get('size')[0])
        count_posts = 'select count(1) count from tb_post where visible = 1 and deleted = 0 and user_id = %s'
        _count = db.get(count_posts, self.current_user.id)
        count = _count.count
        query = """select id, title, content, category_id, created, updated from tb_post
                 where visible = 1 and deleted = 0 and user_id = %s order by if(updated is NULL, created, updated) desc
                 limit 0, %s
                """
        posts = db.query(query, self.current_user.id, size)
        if posts:
            needPagination = True if count > len(posts) else False
            for post in posts:
                _html = markdown.markdown(post.content)
                soup = BeautifulSoup(_html, 'html.parser')
                _text = soup.get_text()
                if _text and len(_text) > 200:
                    _text = _text[0:200] + '...'
                post['summary'] = _text
                post['last_modified'] = post['updated'] if post['updated'] else post['created']
                post['author'] = self.current_user

        self.render('posts.html', posts=posts, pageSize=size, needPagination=int(needPagination))

"""
get curent user's drafts, need login.
"""
class DraftListHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        size = 10
        args = self.request.arguments
        if args.get('size'):
            size = int(args.get('size')[0])
        query = """select id, title, content, user_id, created, updated from tb_post
                 where user_id = %s and deleted = 0 and visible = 0 order by if(updated is NULL, created, updated) desc
                """
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

        self.render('drafts.html', drafts=drafts)

class ListApiHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self, offset=0, size=10):
        res = {'data': None}
        needPagination = False
        args = self.request.arguments
        offset = args.get('offset') and args.get('offset')[0] or offset
        size = args.get('size') and args.get('size')[0] or size

        count_posts = 'select count(1) as count from tb_post where visible = 1 and deleted = 0 and user_id = %s'
        _count = db.get(count_posts, self.current_user.id)
        count = _count.count

        query = """
                select id, title, content, user_id, created, updated from tb_post
                where user_id = %s and deleted = 0 and visible = 1 order by if(updated is NULL, created, updated) desc
                limit %s, %s
                """
        posts = db.query(query, self.current_user.id, int(offset), int(size))
        if posts:
            needPagination = True if count > (int(offset) + int(size)) else False
            for post in posts:
                _html = markdown.markdown(post.content)
                soup = BeautifulSoup(_html, 'html.parser')
                _text = soup.get_text()
                if _text and len(_text) > 200:
                    _text = _text[0:200] + '...'
                post['summary'] = _text
                post['last_modified'] = post['updated'] if post['updated'] else post['created']
                post['author'] = self.current_user
            posts = json.dumps(posts, cls=modules.utils.JSONEncoder)
            res = {'res': {'data': posts, 'needPagination': needPagination}}

        self.write(res)
        self.finish()

"""
get single post by id
"""
class PostHandler(baseHandler.RequestHandler):

    def get(self, id):
        query = """select id, title, content, user_id, public, visible, if(updated is NULL, created, updated) as last_modified
                 from tb_post where id = %s and deleted = 0
                """
        post = db.get(query, id)
        if post:
            if not ord(post.public):
                if not self.current_user:
                    raise tornado.web.HTTPError(403)
                    return
                elif self.current_user.id != post.user_id:
                    raise tornado.web.HTTPError(403)
                    return
            query_author = 'select id, nick from tb_user where id = %s'
            author = db.get(query_author, post.user_id)
            post['author'] = author
            post.content = bleach.clean(markdown.markdown(post.content), tags=settings['white_tags_list'], attributes=settings['white_attrs_list'])
        else:
            raise tornado.web.HTTPError(404)

        self.render('post.html', post=post)

"""
direct to the edit page
"""
class EditHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self, post_id=None):
        post = None
        if post_id:
            get_post = 'select id, title, content, user_id, category_id, public from tb_post where id = %s'
            _post = db.get(get_post, post_id)
            if _post and _post.user_id == self.current_user.id:
                post = _post
        get_categories = 'select id, name from tb_category where visible = 1'
        categories = db.query(get_categories)
        referer = self.request.headers.get('Referer') or '/'

        self.render('edit.html', categories=categories, post=post, referer=referer)

"""
make the post be public
"""
class ShareHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def post(self):
        post_id = self.get_body_argument('post_id')
        query = 'select id, user_id from tb_post where id = %s and deleted = 0'
        _post = db.query(query)
        if _post and _post.id == post_id:
            update_public = 'update tb_post set public = 1 where id = %s'
            row_count = db.update(update_public, post_id)
            if row_count:
                self.write({'success': True})
                self.finish()
                return
            self.write({'success': False})
            self.finish()
            return
        self.write({'success': False})
        self.finish()

"""
create new post or update an exist post
"""
class InsertOrUpdateHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def post(self):
        title = self.get_body_argument('title')
        content = self.get_body_argument('content')
        category_id = self.get_body_argument('category')
        user_id = self.current_user.id
        post_public = self.get_body_argument('privacy')
        post_id = int(self.get_body_argument('id'))
        visible = 1 - int(self.get_body_argument('draft'))

        if title and content and category_id:
            now = datetime.datetime.now()
            if post_id != -1:
                sql = 'update tb_post set title = %s, content = %s, public = %s, visible = %s, category_id = %s, updated = %s where id = %s and deleted = 0'
                num = db.update(sql, title, content, int(post_public), int(visible), int(category_id), now, post_id)
            else:
                sql = 'insert into tb_post (title, content, user_id, category_id, public, visible, created) values (%s, %s, %s, %s, %s, %s, %s)'
                num = db.insert(sql, title, content, long(user_id), int(category_id), int(post_public), int(visible), now)

            if num:
                self.write({'success': True})
                self.finish()
                return
            self.write({'success': False})
            self.finish()
            return
        self.write({'success': False})
        self.finish()

"""
mark post as deleted
"""
class DeleteHandler(baseHandler.RequestHandler):
    def delete(self, post_id):
        delete_post = 'update tb_post set deleted = 1 where id = %s'
        num = db.update(delete_post, post_id)
        if num:
            self.write({'success': True})
            self.finish()
            return
        self.write({'success': False})
        self.finish()

