from tornado.web import Application, RequestHandler
import tornado.ioloop
import json
from tornado_sqlalchemy import SQLAlchemy, SessionMixin
from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint


# database
database_url = "sqlite:///test.db"
db = SQLAlchemy(url=database_url)

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
                "id": self.id,
                "test_number": self.test_number,
                "test_string": self.test_string,
                "test_boolen" :self.test_boolen
        }

db.create_all()

# validate payload/ checking of body paramters
class InvalidJSON(Exception):
    pass

class MissingKey(Exception):
    pass 

class IncorrectData(Exception):
    pass 

def validate_json(body):
    try:
        req_data = json.loads(body.decode())
    except Exception as e:
        raise InvalidJSON("Could not parse payload please send a correct format")

    if "test_number" not in req_data or "test_string" not in req_data:
        raise MissingKey("Missing required field")
    
    if isinstance(req_data["test_number"], int) and isinstance(req_data["test_string"], str):
        raise IncorrectData("Wrong data type received")

    return req_data

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
        # payload validation
        if self.request.body:
            try:
                req_data = validate_json(self.request.body)
                # validate_json(req_data)
                # prining payload in the console
                print(req_data)
            except (InvalidJSON, MissingKey, IncorrectData) as e:
                self.set_status(400)
                self.write(str(e))
                return
            # connect and store in database
            with self.make_session() as session:
                data = Test(**req_data)
                session.add(data)
                session.commit()

            response = {"test": req_data}
            self.write(response)


class SingleTestHandler(SessionMixin, RequestHandler):

    def get(self, id):
        if id:
            with self.make_session() as session:
                data = session.query(Test).filter(Test.id == int(id)).first()
                data = data.to_dict()
        
        response = {"test": data}
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
    
        

    
       