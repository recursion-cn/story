import handlers.baseHandler as base
import handlers.mainHandler as main
import handlers.recordHandler as record

urls = [
    (r'/', main.MainHandler),
    (r'/records', record.ListHandler),
    (r'/records/edit', record.EditHandler),
    (r'/records/create', record.NewHandler),
    (r'.*', base.RequestHandler),
]
