import os
import uuid
import bottle
from hashlib import md5

import pymongo
conn = pymongo.Connection(host='dharma.mongohq.com', port=10037)
db = conn.app17278948
db.authenticate('heroku','9af8372f3bf2169a45a60069c57a8dbd')
users = db.users

# function for DB and session ####################

class User(object):
    def __init__(self, d):
        self.__dict__.update(**d)

    def put(self):
        users.update({'username': self.username}, self.__dict__)

def get_md5(s):
    return md5(s).hexdigest()

def get_user(username):
    u = users.find_one({'username':username})
    return u if not u else User(u)

def create_user(username, password):
    if get_user(username):
        return False
    user_dict = {
                   'username':username,
                   'password':get_md5(get_md5(get_md5('abc'*30 + password))),
                   'req_key':'', 'req_secret':'',
                   'oauth_key':'', 'oauth_secret':'',
                   'screen_name':'', 'tid':'',
                }
    users.insert(user_dict)
    return True

def user_auth(username, password):
    user = get_user(username)
    return False if not user else user.password == get_md5(get_md5(get_md5('abc'*30 + password)))

def get_session():
    return bottle.request.get_cookie('session', secret='coffee')

def create_session(username):
    session = {
                'username':username,
                'sessionid':uuid.uuid4().hex,
              }
    bottle.response.set_cookie('session', session, secret='coffee', max_age=30*24*3600)
    return session

def destroy_session():
    bottle.response.delete_cookie('session', secret='coffee')

def get_user_db():
    session = get_session()
    if not session:
        return None
    return get_user(session['username'])
