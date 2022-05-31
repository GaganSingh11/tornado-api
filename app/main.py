from urllib import request
from tornado.web import Application, RequestHandler
import tornado.ioloop
import json

# database
db = [
    {
        "test_number": 1,
        "test_string": "first test added",
        "test_boolen": False
    }
]

# views
class TestHandler(RequestHandler):
    def get(self):
        self.write({"message" : db})

    def post(self):
        if self.request.body:
            test_byt = self.request.body
            test_dict = json.loads(test_byt.decode('utf-8'))

            db.append(test_dict)

            print(test_dict)
            self.write({"message": test_dict})

class SingleTestHandler(RequestHandler):
    def get(self, id):
        if id:
            print(type(id))
            for item in db:
                if item["test_number"] == int(id):
                    result = item
                else:
                    result = "Test not found"
        print(result)
        self.write({"message": result})
                


# server
def make_app():
    return Application(
        [
            (r"/tests", TestHandler),
            (r"/tests/([^/]+)?", SingleTestHandler)
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
    
        

    
       