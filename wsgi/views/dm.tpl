%# vim: set ft=html ts=2 sts=2 sw=2 et sta:
%include header title='Dm',no_enterbox=True

<p><a href='/dm?type=tome'>message to me</a><br/>
<a href='/dm?type=byme'>message by me</a></p>

<fieldset>
<legend>Direct message: </legend>
<div id='input'>
  <form method='post' action='/update'>
    <input type='hidden' name='type' value='dm'/>
    To: <input type='text' id='name' name='name' value='{{name}}'/><br/>
    <textarea id='twt' name='msg' rows='2'></textarea><br/>
    <input type='submit' value='Send'>
</div>
</fieldset>

% if tp=='tome':
<p><b>Messages to me:</b></p>
% elif tp=='byme':
<p><b>Messages sent by me:</b></p>
% end

% for t in tweets:
<div class='tweet'>
 <span class='avatar'><img src='{{t['imgurl']}}'></span>
 <span class='content'>
 <a href='/user?name={{t['sender']}}'>{{t['sender']}}</a>
 to <a href='/user?name={{t['recipient']}}'>{{t['recipient']}}</a>
 <small>
% if t['del']:
  <a href='##' onclick='del(this,"{{t['id']}}","dm")'>DEL</a>
% else:
  <a href='#' onclick='dm("{{t['sender']}}")'>DM</a>
% end
  {{t['time']}}
 </small>
 <div>{{!t['text']}}</div>
 </span>
</div>
% end

% base = 'dm'
% if tp=='tome' or tp=='byme':
%     base += '?type='+tp
% end
%include pages  base=base,tweets=tweets
%include footer
