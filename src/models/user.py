import uuid
import datetime

from flask import session

from src.common.database import Database
from src.models.blog import Blog


class User(object):
    def __init__(self, email, password, first_name, last_name, _id = None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
        self.first_name = first_name
        self.last_name = last_name


    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls,_id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            #Check the password
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password, first_name, last_name):
        user = cls.get_by_email(email)
        if user is None:
            #user doesnt exist so create it
            new_user = cls(email, password, first_name, last_name)
            new_user.save_to_mongo()
            session["email"] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        #login_valid has been called
        session["email"] = user_email

    @staticmethod
    def logout():
        session["email"] = None


    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        blog = Blog(author = self.email,
                    title = title,
                    description = description,
                    author_id = self._id)

        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title = title,
                      content = content,
                      date = date)


    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())