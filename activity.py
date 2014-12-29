# coding: utf-8
import bottle
from utils import *
from oauth import *
from libs import *

@bottle.route('/activity')
@require_login_oauth
def activity():
    ''' activity '''
    acts = api('activity', include_entities=1, **bottle.request.GET)
    for act in acts:
        if act.action in ('retweet', 'favorite'):
            act.targets = process_tweets(act.targets)
        elif act.action in ('follow', 'list_member_added'):
            act.targets = map(process_user_entities, act.targets)
    return bottle.template('activity', acts=acts)
