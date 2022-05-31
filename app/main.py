from tornado.web import Application, RequestHandler
import tornado.ioloop


class HelloHandler(RequestHandler):
    def get(self):
        self.write({"message" : "Hello World"})





def make_app():
    return Application(
        [
            (r"/", HelloHandler)
        ],
        debug = True,
        autoreload = True
    )



if __name__ == "__main__":
    app = make_app()
    port = 8888
    app.listen(port)
    print(f"Server is listening on 127.0.0.1:{port}")
    tornado.ioloop.IOLoop.current().start()
    
        

    
       