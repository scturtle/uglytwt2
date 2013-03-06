info=document.getElementById('info');
twt=document.getElementById('twt');
id=document.getElementById('id');
rtbtn=document.getElementById('rtbtn');
upbtn=document.getElementById('upbtn');
resetbtn=document.getElementById('reset');
ct=document.getElementById('ct');

// word count
function count(){ ct.value=140-twt.value.length; return ct.value; }

// toggle more menu
function togglemore(){
  t=document.getElementById('more');
  t.style.display = t.style.display=='none'?'block':'none';
}

// get info of a tweet
function getInfo(tid){
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open('get','/getinfo?id='+tid,false);
  xmlhttp.send();
  return JSON.parse(xmlhttp.responseText);
}

function resetall(){
  info.innerHTML='';
  twt.value='';
  id.value='';
  rtbtn.type='hidden';
  upbtn.value='Update';
  resetbtn.type='hidden';
  scrollTo(0,0);
}

function re(tid){
  resetall();
  info.innerHTML='loading...';
  var t=getInfo(tid);
  info.innerHTML='@'+t.name+': '+t.text;
  twt.value='@'+t.name+' '+t.others;
  id.value=tid;
  upbtn.value='Reply';
  resetbtn.type='button';
}

function fav(t,tid){
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open('get','/fav?id='+tid,false);
  t.innerHTML='...';
  xmlhttp.send();
  if(xmlhttp.status==200)
    t.innerHTML=xmlhttp.responseText;
  else
    t.innerHTML='ERR';
}

// verb.
function follow(t,name){
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open('get','/follow?name='+name,false);
  t.innerHTML='...';
  xmlhttp.send();
  if(xmlhttp.status==200)
    t.innerHTML=xmlhttp.responseText;
  else
    t.innerHTML='ERR';
}

// verb.
function listm(t,lid,name){
  var xmlhttp=new XMLHttpRequest();
  var action=t.checked?'add':'remove';
  xmlhttp.open('get','/listm?name='+name+'&list_id='+lid+'&action='+action,false);
  t.disabled=true;
  xmlhttp.send();
  t.disabled=false;
}

// verb.
function del(t,tid){
  tp=arguments[2]?arguments[2]:"";
  if(t.innerHTML=='DEL'){
    t.innerHTML='SURE';
  }else{
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.open('get','/del?id='+tid+'&type='+tp,false);
    t.innerHTML='...';
    xmlhttp.send();
    if(xmlhttp.status==200)
      self.location.reload();
    else
      t.innerHTML='ERR';
  }
}

// offical RT
function ort(tid){
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open('get','/ort?id='+tid,false);
  xmlhttp.send();
  if(xmlhttp.status==200)
    self.location='/home';
  else
    info.innerHTML=xmlhttp.responseText;
}

function dm(name){
  document.getElementById('name').value=name;
}

function rt(tid){
  resetall();
  info.innerHTML='loading...';
  var t=getInfo(tid);
  info.innerHTML='';
  twt.value='RT @'+t.name+': '+t.text;
  id.value=tid;
  if(!t.protected){
    rtbtn.type='button';
    rtbtn.onclick=function(){ort(tid);};
  }
  upbtn.value='Retweet';
  resetbtn.type='button';
}

function update(){
  // ajax form post
  form=document.forms[0];
  var params=new Array();
  for(var i=0;i<form.elements.length;i++){
    var p=encodeURIComponent(form.elements[i].name);
    if(!p) continue;
    p+="=";
    p+=encodeURIComponent(form.elements[i].value);
    params.push(p);
  }
  params=params.join("&");
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open('post','/update',false);
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.setRequestHeader("Content-length", params.length);
  xmlhttp.setRequestHeader("Connection", "close");
  xmlhttp.send(params);
  if(xmlhttp.status==200)
    self.location='/home';
  else
    info.innerHTML=xmlhttp.responseText;
}
// vim:set ts=2 sts=2 sw=2 et sta:
