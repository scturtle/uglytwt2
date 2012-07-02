import os
import uuid
import bottle
import pymongo

# function for DB and session ####################

#  settings for mongoDB ##########################

mongo_con = pymongo.Connection(
        os.environ['OPENSHIFT_NOSQL_DB_HOST'],
        int(os.environ['OPENSHIFT_NOSQL_DB_PORT']))

mongo_db = mongo_con[os.environ['OPENSHIFT_APP_NAME']]
mongo_db.authenticate(
        os.environ['OPENSHIFT_NOSQL_DB_USERNAME'],
        os.environ['OPENSHIFT_NOSQL_DB_PASSWORD'])

bottle.TEMPLATE_PATH.append(
  os.path.join(os.environ['OPENSHIFT_GEAR_DIR'],
               'runtime/repo/wsgi/views/'))

#  user functions for mongoDB ####################
def get_md5(s):
    from md5 import md5
    return md5(s).hexdigest()

def get_user(username):
    return mongo_db.users.find_one({'username': username})

def create_user(username, password):
    if get_user(username):
        return 'exists'
    user = {
            'username':username,
            'password':get_md5(get_md5(get_md5(password))),
            }
    mongo_db.users.insert(user)
    return user

def user_auth(username,password):
    user = get_user(username)
    if not user: return False
    return user['password'] == get_md5(get_md5(get_md5(password)))

#  session functions  ############################
def get_session():
    return bottle.request.get_cookie('session',secret='coffee')

def create_session(username):
    session = {
            'username':username,
            'sessionid':uuid.uuid4().hex
            }
    bottle.response.set_cookie('session', session, secret='coffee', max_age=30*24*3600)
    return session

def destroy_session():
    bottle.response.delete_cookie('session', secret='coffee')

