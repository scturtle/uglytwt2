from utils import *
import tweepy
import bottle

# app info #######################################

consumer_key = 'k6h2GKL2ZqTjxxrBZuMEmQ'
consumer_secret = '9CW8b1hVN3kQf6bvPrrgff8TUyehtDyOe9cDj2K5uxA'
domain = 'https://uglytwt2-scturtle.rhcloud.com/'

#  twitter oauth functions  ######################

@bottle.route('/oauth')
def oauth():
    ''' reminder page for oauth '''
    if not get_session(): bottle.redirect('/')
    return bottle.template('oauth')


def get_auth():
    ''' get saved oauth info '''
    username = get_session()['username']
    user = mongo_db.users.find_one({'username': username})
    if 'key' not in user:
        return None
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(user['key'],user['secret'])
    return auth

@bottle.route('/oauth_request')
def oauth_request():
    ''' send oauth request and redirect to twitter '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, domain + 'oauth_callback')
    redirect_url = auth.get_authorization_url()
    username = get_session()['username']
    user = mongo_db.users.find_one({'username': username})
    user['req_key'] = auth.request_token.key
    user['req_secret'] = auth.request_token.secret
    mongo_db.users.update({'username': username}, user)
    bottle.redirect(redirect_url)

@bottle.route('/oauth_callback')
def oauth_callback():
    ''' callback from twitter and save oauth info '''
    verifier = bottle.request.GET['oauth_verifier']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    username = get_session()['username']
    user = mongo_db.users.find_one({'username': username})
    auth.set_request_token(user['req_key'], user['req_secret'])
    auth.get_access_token(verifier)
    del user['req_key']
    del user['req_secret']
    user['key'] = auth.access_token.key
    user['secret'] = auth.access_token.secret
    user['tid'] = tweepy.API(auth).me().id_str
    mongo_db.users.update({'username': username}, user)
    bottle.redirect('/home')

@bottle.route('/unoauth')
def unoauth():
    ''' delete oauth info '''
    username = get_session()['username']
    user = mongo_db.users.find_one({'username': username})
    del user['key']
    del user['secret']
    del user['tid']
    mongo_db.users.update({'username': username}, user)
    bottle.redirect('/oauth')

