import handlers.baseHandler as base
import handlers.mainHandler as main
import handlers.postHandler as post
import handlers.userHandler as user
import handlers.categoryHandler as cate
import handlers.api.postApiHandler as postApi

urls = [
    (r'/', main.IndexHandler),
    (r'/site/(\w+)', main.IndexHandler),
    (r'/users/login', user.LoginHandler),
    (r'/users/signup', user.SignupHandler),
    (r'/users/exit', user.LogoutHandler),
    (r'/users/draft', post.DraftListHandler),
    (r'/users/edit', post.EditHandler),
    (r'/users/edit/(\d+)', post.EditHandler),
    (r'/users/setting', user.SettingHandler),
    (r'/users/profile/(\d+)', user.ProfileHandler),
    (r'/api/users/change_password', user.PasswordModifyHandler),
    (r'/posts', post.ListHandler),
    (r'/api/posts', post.ListApiHandler),
    (r'/api/posts/like', postApi.LikeHandler),
    (r'/posts/(\d+)', post.PostHandler),
    (r'/api/posts/(\d+)', postApi.PostHandler),
    (r'/posts/create', post.InsertOrUpdateHandler),
    (r'/posts/delete/(\d+)', post.DeleteHandler),
    (r'/category/exist', cate.IsCategoryExistHandler),
    (r'/category/add', cate.AddHandler),
    (r'/api/category/delete', cate.BatchDeleteHandler),
    (r'/invite', main.InviteHandler),
    (r'.*', base.RequestHandler),
]
