%# vim: set ts=2 sts=2 sw=2 et sta:
% for t in tweets:
<div class='tweet'>
 <span class='avatar'><img src='{{t['imgurl']}}'></span>
 <span class='content'>
 <a href='/user?name={{t['name']}}'>{{t['name']}}</a>
 <small>
  <a href='#' onclick='re("{{t['id']}}")'>@</a>
  <a href='##' onclick='fav(this,"{{t['id']}}")'>{{'UNFAV' if t['fav'] else 'FAV'}}</a>
  <a href='#' onclick='rt("{{t['id']}}")'>RT</a>
% if t['del']:
  <a href='##' onclick='del(this,"{{t['id']}}")'>DEL</a>
% end
  {{t['time']}}
 </small>
 <div>
  {{!t['text']}}
  <small>via {{t['source']}} {{!t['RTinfo']}} 
% if t['thread']:
  <a href='/thread?id={{t['id']}}'>thread</a>
% end
  </small>
 </div>
 </span>
</div>
% end
