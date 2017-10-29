import datetime

from src.common.database import Database
from src.models.blog import Blog

Database.initialize()

p = Blog.from_mongo('12345')
print(p)


