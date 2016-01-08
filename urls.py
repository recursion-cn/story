import handlers.baseHandler as base
import handlers.mainHandler as main
import handlers.postHandler as post
import handlers.userHandler as user
import handlers.categoryHandler as cate
import handlers.fileHandler as file
import handlers.api.postApiHandler as post_api

main_url = [
    (r'/', main.IndexHandler),
    (r'/site/(\w+)', main.IndexHandler),
    (r'/invite', main.InviteHandler),
    (r'.*', base.RequestHandler),
]

api_url = [
    (r'/api/users/change_password', user.PasswordModifyHandler),
    (r'/api/posts', post.ListApiHandler),
    (r'/api/posts/(\d+)', post_api.PostHandler),
    (r'/api/posts/like', post_api.LikeHandler),
    (r'/api/category/delete', cate.BatchDeleteHandler),
    (r'/api/invite/code', main.InviteGenerateHandler),
]

users_url = [
    (r'/users/login', user.LoginHandler),
    (r'/users/signup', user.SignupHandler),
    (r'/users/exit', user.LogoutHandler),
    (r'/users/draft', post.DraftListHandler),
    (r'/users/edit', post.EditHandler),
    (r'/users/edit/(\d+)', post.EditHandler),
    (r'/users/setting', user.SettingHandler),
    (r'/users/profile/(\d+)', user.ProfileHandler),
]

posts_url = [
    (r'/posts', post.ListHandler),
    (r'/posts/(\d+)', post.PostHandler),
    (r'/posts/create', post.InsertOrUpdateHandler),
    (r'/posts/delete/(\d+)', post.DeleteHandler),
]

cates_url = [
    (r'/category/exist', cate.IsCategoryExistHandler),
    (r'/category/add', cate.AddHandler),
]

files_url = [
    (r'/files/upload', file.FileHandler),
]

urls = api_url + users_url + posts_url + cates_url + files_url
urls += main_url
