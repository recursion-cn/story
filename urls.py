import handlers.baseHandler as base
import handlers.mainHandler as main
import handlers.postHandler as post
import handlers.userHandler as user

urls = [
    (r'/', main.MainHandler),
    (r'/users/login', user.LoginHandler),
    (r'/users/signup', user.SignupHandler),
    (r'/posts', post.ListHandler),
    (r'/posts/(\d+)', post.PostHandler),
    (r'/posts/edit', post.EditHandler),
    (r'/posts/create', post.NewHandler),
    (r'.*', base.RequestHandler),
]
