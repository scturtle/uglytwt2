import os
import uuid
import bottle

from google.appengine.api import users
from google.appengine.ext import db

# function for DB and session ####################

class User(db.Model):
    user = db.UserProperty()
    req_key = db.StringProperty()
    req_secret = db.StringProperty()
    oauth_key = db.StringProperty()
    oauth_secret = db.StringProperty()
    screen_name = db.StringProperty()
    tid = db.StringProperty()

def get_user_db():
    user = get_session()
    if not user:
        return None
    else:
        user_db = db.Query(User).filter('user =',user).get()
        if not user_db:
            user_db = User(user=user)
            user_db.put()
        return user_db

def get_session():
    return users.get_current_user()
