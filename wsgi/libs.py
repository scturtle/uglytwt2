import tweepy
from utils import *
from oauth import *
import datetime

def require_login_oauth(func):
    ''' wrapper for check session and oauth '''
    def wrapper(*a, **ka):
        if not get_session(): 
            return bottle.redirect('/')
        if not get_auth(): 
            return bottle.redirect('/oauth')
        return func(*a, **ka)
    return wrapper

def api(method,**argv):
    ''' wrapper for tweepy api '''
    if not get_session(): return None
    auth = get_auth()
    if not auth: return None
    if not method: return None
    #if method in ['home_timeline']:
        #argv['count']=20
    if method in ['home_timeline','user_timeline','list_timeline',
            'favorites','mentions','get_status','search',
            'direct_messages', 'sent_direct_messages']:
        argv['include_entities']=1
        argv['include_rts']=1
    method = getattr(tweepy.API(auth), method, None)
    tweets = method(**argv)
    return tweets

def replace_all(text,rep_list):
    ''' for process_entities '''
    for l in rep_list:
        text = text[:l[1][0]]+l[0]+text[l[1][1]:]
    return text

def process_entities(tweet):
    ''' process entities: tags, urls, users, pics ''' 
    if hasattr(tweet,'entities'):
        ent = tweet.entities
        rep_list=[]
        # hashtags
        if 'hashtags' in ent:
            for t in ent['hashtags']:
                m = '<a class="tag" href="/search?q=%%23%s">#%s</a>' % (t['text'],t['text'])
                rep_list.append((m, t['indices']))
        # urls
        if 'urls' in ent:
            for u in ent['urls']:
                if 'display_url' in u:
                    ue,ud = u['expanded_url'], u['display_url']
                else:
                    ue = ud = u['url']
                m = '<a href="%s" target=_blank>%s</a>' % (ue, ud)
                rep_list.append((m, u['indices']))
        # media
        if 'media' in ent:
            for md in ent['media']:
                # if md['type']=='photo'
                m = '<a href="%s" target=_blank>%s</a>' %\
                        (md['media_url'], '[p.twimg.com]')
                rep_list.append((m, md['indices']))

        # user_mentions
        if 'user_mentions' in ent:
            for u in ent['user_mentions']:
                name = u['screen_name']
                url = '/user?name=' + name
                m = '<a href="%s">@%s</a>' % (url, name)
                rep_list.append((m, u['indices']))

        # replace backwards
        rep_list.sort(key=lambda x: x[1][0],reverse=True)
        return replace_all(tweet.text, rep_list)
    return tweet.text

def process_dm(tweet):
    ''' preprocess direct message '''
    t={}
    user = mongo_db.users.find_one({'username': get_session()['username']})
    t['time'] = str(tweet.created_at+datetime.timedelta(hours=+8))[5:16]
    t['del'] = str(tweet.sender_id) == user['tid']
    t['id'] = tweet.id_str
    t['imgurl'] = tweet.sender.profile_image_url.replace('normal.','mini.')
    t['sender'] = tweet.sender_screen_name
    t['recipient'] = tweet.recipient_screen_name
    t['text'] = process_entities(tweet)
    return t
    

def process_tweet(tweet):
    ''' preprocess tweet '''
    t = {}
    RTed = False
    if hasattr(tweet,'retweeted_status'):
        RTed = True
        old_tweet = tweet
        tweet = tweet.retweeted_status
        t['RT_oldId']=old_tweet.id_str
    user = mongo_db.users.find_one({'username': get_session()['username']})
    if hasattr(tweet, 'author'):
        t['imgurl'] = tweet.author.profile_image_url.replace('normal.','mini.')
        t['name'] = tweet.author.screen_name
        t['del'] = tweet.author.id_str == user['tid']
    else: # for search result
        t['imgurl'] = tweet.profile_image_url.replace('normal.','mini.')
        t['name'] = tweet.from_user
        t['del'] = tweet.from_user_id_str == user['tid']
    t['id'] = tweet.id_str
    t['fav'] = tweet.favorited if hasattr(tweet,'favorited') else False
    t['time'] = str(tweet.created_at+datetime.timedelta(hours=+8))[5:16]
    t['text'] = process_entities(tweet)
    t['source'] = tweet.source
    t['RTinfo'] = ''
    if RTed or (hasattr(tweet,'retweet_count') and tweet.retweet_count):
        if RTed: # by your following people
            t['RTinfo'] = 'RT by ' + old_tweet.author.screen_name
            count = tweet.retweet_count
            if type(count)==unicode and count[-1]=='+': # '100+'
                t['RTinfo'] += ' and %s others' % count
            else: # regular number
                count = int(count) - 1
                if count>0:
                    t['RTinfo'] += ' and %d others' % count
        else: # by others
            t['RTinfo'] = 'RT by %s users' % str(tweet.retweet_count)
    t['thread'] = bool(hasattr(tweet,'in_reply_to_status_id_str') and tweet.in_reply_to_status_id_str)
    return t

