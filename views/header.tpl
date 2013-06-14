%# vim: set ts=2 sts=2 sw=2 et sta:
<!doctype html>
<html>
  <head>
    <meta charset=utf-8>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta name="format-detection" content="telephone=no" />
    <title>{{title}}</title>
    <link rel="stylesheet" href="/static/main.css" type="text/css"/>
  </head>
  <body>
    % if not defined('no_nav'):
    <div>
    <ul class='nav even-5' id='nav'>
      <li><a href='/home'>home</a></li>
      <li><a href='/me'>me</a></li>
      <li><a href='/mention'>@me</a></li>
      <li><a href='/search'>search</a></li>
      <li><a onclick='togglemore()' href='#'>more</a></li>
    </ul>

    <ul style='display:none' class='nav even-5' id='more'>
      <li><a href='/dm'>dm</a></li>
      <li><a href='/list'>list</a></li>
      <li><a href='/activity'>activity</a></li>
      <li><a href='/favs'>fav</a></li>
      <li><a href='/exit'>exit</a></li>
    </ul>
    </div>
    % end
    % if not defined('no_enterbox'):
    <div id='input'>
      <small><div id='info'></div></small>
      tweet:
      <form>
        <textarea id="twt" name="twt" rows="4" onkeydown='count()' onkeyup='count()'></textarea>
        <input id='id'   name='id'   type='hidden' value='' />
        <input id='rtbtn' type='hidden' value='Offical RT' />
        <input id='upbtn' type='button' value='Update' onclick='update()'/>
        <input id='reset' type='hidden' value='Reset' onclick='resetall()'/>
	<input id='ct' type='button' value='140' onclick='count()'/>
      </form>
    </div>
    % end
