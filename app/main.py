from tornado.web import Application, RequestHandler
import tornado.ioloop
import json
from tornado_sqlalchemy import SQLAlchemy, SessionMixin
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint


# database
database_url = "sqlite:///test.db"
db = SQLAlchemy(url=database_url)
# engine = create_engine(database_url)

# database model
class Test(db.Model):
    __tablename__ = "tests"

    id = Column(Integer, nullable=False, primary_key=True)
    test_number = Column(Integer, nullable=False)
    test_string = Column(String(100), nullable=False)
    test_boolen = Column(Boolean, nullable=True, default=False)
    UniqueConstraint(test_string)

    def to_dict(self):
        return {
                "test_number": self.test_number,
                "test_string": self.test_string,
                "test_boolen" :self.test_boolen
        }

db.create_all()


db_list = [
    {
        "test_number": 1,
        "test_string": "first test added",
        "test_boolen": False
    }
]

# views
class TestHandler(SessionMixin, RequestHandler):
    
    def get(self):
        with self.make_session() as session:
            data = []
            for test in session.query(Test):
                data.append(test.to_dict())
        response = {"tests": data}
        self.write(response)

    def post(self):
        if self.request.body:
            with self.make_session() as session:
                test_byt = self.request.body
                test_dict = json.loads(test_byt.decode('utf-8'))
                print(test_dict)
                data = Test(**test_dict)
                session.add(data)
                session.commit()

            response = test_dict
            self.write(response)


class SingleTestHandler(SessionMixin, RequestHandler):

    def get(self, id):
        if id:
            with self.make_session() as session:
                data = session.query(Test).filter(Test.id == int(id)).first()
                data = data.to_dict()
        
        response = data
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
        db = SQLAlchemy(database_url)
    )



if __name__ == "__main__":
    app = make_app()
    port = 8888
    app.listen(port)
    print(f"Server is listening on 127.0.0.1:{port}")
    tornado.ioloop.IOLoop.current().start()
    
        

    
       