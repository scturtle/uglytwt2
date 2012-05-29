UglyTwT2
========

another ugly twitter web client for mobile

Require
-----------

This project is builded on Openshift of RedHat but may also suit for GAE or a VPS.

* Python 2.6+
* Bottle
* Tweepy
* Pymongo
* MongoDB

Install
--------

Just create a app of Python and MongoDB on Openshift and `git clone` it. Then replace origin files with this project files and `git push` it.   
Oauth infomations are in `oauth.py`. DB infomations are in `utils.py`.   
You can refer to my [blog](http://scturtle.is-programmer.com/posts/33787.html) about "How to play Openshift".