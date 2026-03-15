from sqlalchemy.engine import make_url
import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")
print("RAW:", repr(DB_URI))

url = make_url(DB_URI)
print("drivername:", url.drivername)
print("username:", url.username)
print("host:", repr(url.host))
print("port:", url.port)
print("database:", url.database)
print("*"*30)
print("RAW:", repr(DB_URI))
print("host:", repr(url.host))
print("drivername:", url.drivername)