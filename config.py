import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.db")
# use this if you want app to crash if settings not present while the above can still default to sqlite
# SQLALCHEMY_DATABASE_URI = os.environ.get["DATABASE_URL"]
