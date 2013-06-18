%# vim: set ts=2 sts=2 sw=2 et sta:
%include header title=title, no_enterbox=True
<p><b>list memberships of 
<a href='/user?name={{name}}'>@{{name}}</a>:</b></p>
% for r in result:
<input type="checkbox" {{'checked' if r[1] else ''}} onchange='listm(this,"{{r[0].id_str}}","{{name}}")'> {{r[0].name}} <br>
%end
%include footer
