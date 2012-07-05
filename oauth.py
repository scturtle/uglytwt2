from utils import *
import tweepy
import bottle

from google.appengine.api import users
from google.appengine.ext import db

# app info #######################################

consumer_key = 'k6h2GKL2ZqTjxxrBZuMEmQ'
consumer_secret = '9CW8b1hVN3kQf6bvPrrgff8TUyehtDyOe9cDj2K5uxA'
domain = 'https://uglytwtr.appspot.com/'

#  twitter oauth functions  ######################

@bottle.route('/oauth')
def oauth():
    ''' reminder page for oauth '''
    if not get_session(): bottle.redirect('/')
    return bottle.template('oauth')


def get_auth():
    ''' get saved oauth info '''
    user = get_user_db()
    if not user.oauth_key:
        return None
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(user.oauth_key,user.oauth_secret)
    return auth

@bottle.route('/oauth_request')
def oauth_request():
    ''' send oauth request and redirect to twitter '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, domain + 'oauth_callback')
    redirect_url = auth.get_authorization_url()
    user = get_user_db()
    user.req_key = auth.request_token.key
    user.req_secret = auth.request_token.secret
    user.put()
    bottle.redirect(redirect_url)

@bottle.route('/oauth_callback')
def oauth_callback():
    ''' callback from twitter and save oauth info '''
    verifier = bottle.request.GET['oauth_verifier']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    user = get_user_db()
    auth.set_request_token(user.req_key, user.req_secret)
    auth.get_access_token(verifier)
    user.oauth_key = auth.access_token.key
    user.oauth_secret = auth.access_token.secret
    me = tweepy.API(auth).me()
    user.screen_name = me.screen_name
    user.tid = me.id_str
    user.put()
    bottle.redirect('/home')

@bottle.route('/unoauth')
def unoauth():
    ''' delete oauth info '''
    user = get_user_db()
    user.oauth_key=''
    user.oauth_secret=''
    user.screen_name = ''
    user.tid=''
    user.put()
    bottle.redirect('/oauth')

