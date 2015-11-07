import handlers.baseHandler as base
import handlers.mainHandler as main
import handlers.postHandler as post
import handlers.userHandler as user

urls = [
    (r'/', main.MainHandler),
    (r'/users/login', user.LoginHandler),
    (r'/users/signup', user.SignupHandler),
    (r'/users/exit', user.LogoutHandler),
    (r'/users/draft', post.DraftListHandler),
    (r'/users/edit/(\d?)', post.EditHandler),
    (r'/posts', post.ListHandler),
    (r'/posts/(\d+)', post.PostHandler),
    (r'/posts/create', post.NewHandler),
    (r'.*', base.RequestHandler),
]
