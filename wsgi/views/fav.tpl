%# vim: set ts=2 sts=2 sw=2 et sta:
%include header title='Favorites'
<p><b>favorites of {{name}}:</b></p>
%include tweets tweets=tweets
%include pages  base='favs?name='+name,tweets=tweets
%include footer
