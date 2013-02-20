%# vim: set ts=2 sts=2 sw=2 et sta:
%include header title='List'
% if only_slugs:
<p><b>lists of {{owner}}:</b></p>
% for l in slugs:
<p><a href='/list?owner={{l[0]}}&slug={{l[1]}}'>{{l[2]}}</a></p>
%end
%else:
<p><b>list {{owner}}/{{slug}}:</b></p>
%include tweets tweets=tweets
%import urllib
%include pages  base='list?owner=%s&slug=%s' % (owner,urllib.quote_plus(slug)), tweets=tweets
%end
%include footer
