import bottle
from utils import *
from oauth import *
from libs import *

@bottle.route('/dm')
@require_login_oauth
def user():
    ''' direct messages page '''
    if 'name' in bottle.request.GET:
        name = bottle.request.GET.get('name')
        bottle.request.GET.pop('name')
    else:
        name =''
    if 'type' in bottle.request.GET:
        tp = bottle.request.GET.get('type')
        bottle.request.GET.pop('type')
    else:
        tp = ''

    if tp == 'tome':
        tweets = api('direct_messages', **bottle.request.GET)
    elif tp == 'byme':
        tweets = api('sent_direct_messages', **bottle.request.GET)
    else:
        tweets = []

    tweets = process_dms(tweets)
    return bottle.template('dm', name = name, tp = tp, tweets = tweets)
