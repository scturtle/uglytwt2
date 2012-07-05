%# vim: set ts=2 sts=2 sw=2 et sta:
%include header title='mention'
<p><b>mentions to me:</b></p>
%include tweets tweets=tweets
%include pages  base='mention',tweets=tweets
%include footer
