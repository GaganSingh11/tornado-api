from tornado.web import Application, RequestHandler
import tornado.ioloop
import json
from tornado_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint


# database
database_url = "sqlite:///test.db"
db = SQLAlchemy(url=database_url)
engine = create_engine(database_url)

# database model
class Test(db.Model):
    __tablename__ = "tests"

    test_number = Column(Integer, nullable=False, primary_key=True)
    test_string = Column(String, nullable=False)
    test_boolen = Column(Boolean, nullable=True)
    UniqueConstraint(test_string)


db_list = [
    {
        "test_number": 1,
        "test_string": "first test added",
        "test_boolen": False
    }
]

# views
class TestHandler(RequestHandler):
    
    def get(self):

        response = {"all posts": db_list}
        self.write(response)

    def post(self):
        if self.request.body:
            test_byt = self.request.body
            test_dict = json.loads(test_byt.decode('utf-8'))

            db_list.append(test_dict)

            print(test_dict)
            response = test_dict
            self.write(response)


class SingleTestHandler(RequestHandler):

    def get(self, id):
        if id:
            print(type(id))
            for item in db_list:
                if item["test_number"] == int(id):
                    result = item
                else:
                    result = "Test not found"
        print(result)
        response = result
        self.write(response)
                


# server
def make_app():
    return Application(
        [
            (r"/tests", TestHandler),
            (r"/tests/([^/]+)?", SingleTestHandler)
        ],
        debug = True,
        autoreload = True,
        db = SQLAlchemy(database_url, binds=engine)
    )



if __name__ == "__main__":
    app = make_app()
    port = 8888
    app.listen(port)
    print(f"Server is listening on 127.0.0.1:{port}")
    tornado.ioloop.IOLoop.current().start()
    
        

    
       