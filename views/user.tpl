%# vim: set ts=2 sts=2 sw=2 et sta:
%include header title='User'
%include userinfo users=[user],is_following_me=is_following_me
% if tweets!=None:
%include tweets tweets=tweets
%include pages  base='user?name='+user.screen_name,tweets=tweets
% else:
<p>Protected.</p>
% end
%include footer
