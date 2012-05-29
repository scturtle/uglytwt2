%# vim: set ts=2 sts=2 sw=2 et sta:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
    <title>{{title}}</title>
    <link rel="stylesheet" href="/static/main.css" type="text/css"/>
  </head>
  <body>
    % if not defined('no_nav'):
    <div id='nav'>
      <a href='/home'>home</a> <a href='/me'>me</a> <a href='/mention'>@me</a> 
      <a href='/list'>list</a> <a href='/favs'>fav</a> <a href='/exit'>exit</a>
    </div>
    % end
    % if not defined('no_enterbox'):
    <div id='input'>
      <small><span id='info'></span></small>
      <form>
        <textarea id="twt" name="twt" rows="3"></textarea>
        <input id='type' name='type' type='hidden' value='' />
        <input id='id'   name='id'   type='hidden' value='' />
        <input id='rtbtn' type='hidden' value='Offical RT' />
        <input id='upbtn' type='button' value='Update' onclick='update()'/>
        <input id='reset' type='hidden' value='Reset' onclick='resetall()'/>
      </form>
    </div>
    % end
