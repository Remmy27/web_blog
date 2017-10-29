import uuid
import datetime
from src.common.database import Database


class Post(object):
    def __init__(self, blog_id,  title, content, author, date = datetime.datetime.utcnow(), _id = None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.date = date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection = "posts",
                        data = self.json())

    def json(self):
        return {
            "_id": self._id,
            "blog_id": self.blog_id,
            "author": self.author,
            "content": self.content,
            "title": self.title,
            "date": self.date
        }
    @classmethod
    def from_mongo(cls, id):
        # Post.from_mongo(id)
        post_data =  Database.find_one(collection = "posts", query = {"_id": id})
        return cls(**post_data)

    @staticmethod
    def from_blog(id):
        return [p for p in Database.find(collection = "posts", query = {"blog_id" : id})]


