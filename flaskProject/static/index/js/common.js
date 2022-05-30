var user;
if (document.cookie.length > 0) {
	var offset = document.cookie.indexOf("_user=");
	if (offset > -1) {
		offset += 6;
		var end = document.cookie.indexOf(";", offset);
		if (end == -1) end = document.cookie.length;
		user = JSON.parse(unescape(document.cookie.substring(offset, end)));
	}
}

var mobileAgent = new Array("iphone", "ipod", "ipad", "android", "mobile", "blackberry", "webos", "incognito", "webmate", "bada", "nokia", "lg", "ucweb", "skyfire");
var browser = navigator.userAgent.toLowerCase();
for (var i=0; i<mobileAgent.length; i++){
	if (browser.indexOf(mobileAgent[i])!=-1){
		if(window.location.href.indexOf('www.caimoge.net') > 0) {
			window.location.href = window.location.href.replace('www.caimoge.net', 'm.caimoge.net');
		}
		break;
	}
}
//用户验证
function setCookie(name, value) {
	var exp = new Date();
	exp.setTime(exp.getTime() + 30 * 24 * 60 * 60 * 1000);
	document.cookie = name + '=' + escape(value) + ';expires=' + exp.toGMTString() + '; path=/';
}
function getCookie(name) {
	var arr = document.cookie.match(new RegExp('(^| )' + name + '=([^;]*)(;|$)'));
	if (arr != null) return unescape(arr[2]);
	return null;
}
//登录状态
function login() {
	if (user) {
		document.write('<div class="status">用户名：<em>'+user.name+'</em> <a href="/history.html">用户中心</a> | <a href="/logout.html">退出登录</a></div>');
	} else {
		document.write('<div class="login"><form name="framelogin" method="post" action="/login.html">账 号：<input type="text" name="username" class="input" value="" size="10" maxlength="30" /> 密 码：<input type="password" name="password" class="input" /> <input type="checkbox" name="cookielife" value="2592000" class="checkbox" checked="check" /> 自动登录 <input type="hidden" name="action" value="login" /><input type="submit" name="submit" class="button" value=" " /><em> <a href="/register.html">注册账户</a></em></form></div>');
	}
}
//获取今日日期
function getToday() {
	var date = new Date();
	var year = date.getFullYear();
	var month = date.getMonth()+1;
	var day = date.getDate();
	if (month < 10) month = '0' + month;
	if (day < 10) day = '0' + day;
	return year+month+day;
}
//cookie读取
function get_cookie_value(Name) {
	var search = Name + "=";
	var returnvalue = "";
	if (document.cookie.length > 0) {
		offset = document.cookie.indexOf(search);
		if (offset != -1) {
			offset += search.length
			end = document.cookie.indexOf(";", offset);
			if (end == -1) end = document.cookie.length;
			returnvalue=document.cookie.substring(offset, end);
		}
	}
	return returnvalue;
}
//ajax获取
function get_ajax_data(url) {
	var xmlhttp;
	xmlhttp=null;
	if (window.XMLHttpRequest) {
		xmlhttp=new XMLHttpRequest();
	} else if (window.ActiveXObject) {
		try {
			xmlhttp=new ActiveXObject("Msxml2.XMLHTTP");
		} catch(e) {
			xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
		}
	}
	if (xmlhttp!=null) {
		xmlhttp.open("GET", url, false);
		xmlhttp.send(null);
		if (xmlhttp.readyState==4) {
			if(xmlhttp.status==200) {
				var json = eval('(' + xmlhttp.responseText + ')');
				return json;
			} else {
				alert("AJAX 请求失败！");
				return false;
			}
		}
	} else {
		alert("浏览器不支持 AJAX！");
		return false;
	}
}
/*history*/
function gethistory() {
	var log = localStorage.getItem("jieqiHistory");
	var list = [];
	if ("string" != typeof log || "" === log) return list;
	var reg = /^\d+\-.+?\-\d+\-.*?\-\d{10}$/;
	var ilist = log.split('|');
	for (var i = 0; i < ilist.length; i++) {
		if (reg.test(ilist[i])) list.push(ilist[i]);
	}
	return list;
}
function sethistory(aid,aname,cid,cname) {
	if (!aid || !aname) return;
	cid = cid || 0;
	cname = cname || '';
	var log = gethistory();
	var time = Math.floor(new Date().getTime()/1000);
	if (log.length == 0) return localStorage.setItem("jieqiHistory", aid+'-'+escape(aname)+'-'+cid+'-'+escape(cname)+'-'+time);
	var rhistory = [];
	for (var i = 0; i < log.length; i++) {
		if (log[i].indexOf(aid+'-') !== 0) rhistory.push(log[i]);
	}
	rhistory.push(aid+'-'+escape(aname)+'-'+cid+'-'+escape(cname)+'-'+time);
	localStorage.setItem("jieqiHistory", rhistory.join('|'));
}
function delhistory(aid) {
	var log = gethistory();
	var rhistory = [];
	for (var i = 0; i < log.length; i++) {
		if (log[i].indexOf(aid+'-') !== 0) rhistory.push(log[i]);
	}
	localStorage.setItem("jieqiHistory", rhistory.join('|'));
	//remove
}
function readhistory(aid) {
	var log = gethistory();
	for (var i = 0; i < log.length; i++) {
		if (log[i].indexOf(aid+'-') === 0) {
			var read = log[i].match(/^(\d+)\-(.+?)\-(\d+)\-(.*?)\-\d{10}$/);
			document.writeln('<li><span>读到</span><i></i><a href="/read/'+read[1]+'/'+read[3]+'.html">'+unescape(read[4])+'</a></li>');
		}
	}
}
function showhistory(num) {
	num = num || 50;
	var log = gethistory();
	if (log.length > 0){
		var list = log.reverse();
		for (var i = 0; i < list.length && i < num; i++) {
			var read = list[i].split('-');
			document.writeln('<ul id="s'+i+'">');
			document.writeln('<li class="two">'+unescape(read[1]));
			document.writeln('<li class="three"><a href="/read/'+read[0]+'/'+read[2]+'.html">'+unescape(read[3])+'</a></li>');
			document.writeln('</ul>');
		}
	}
}
//标记书签
function addMark(name,zhang){
	alert('标记成功'+'<'+name+'>'+'--'+zhang);
}
//二维码
function erweima(id){
document.write("<a href=\"https://m.caimoge.net/txt/" + id + ".html\" target=\"_blank\"><img src=\"https://api.qrserver.com/v1/create-qr-code/?size=150x150&margin=10&data=http://m.caimoge.net/txt/" + id + ".html\" alt=\"{=C('site.name')}手机版二维码\" /></a>"+"<p>扫描二维码下载本书</p>");
}
// 搜索点击事件
function serBtn(){
	var serbtn = document.getElementById('serBtn');
	var inputformq = document.getElementById('inputformq');
	serbtn.onclick=function(){
		if (inputformq.value==""){
			alert("内容不能为空!")
			return false;
			}
			else
			{
			return true;
			}
		return true;
	}	
}
//判断是否登录

function hengfu(){
}
//sort_list 分类当前位置
function navTab(){
	var urlstr = location.href;
	var urlstatus=false;
	$("#zpfl_list a").each(function () {
    if ((urlstr + '/').indexOf($(this).attr('href')) > -1&&$(this).attr('href')!='') {
      $(this).addClass('cur');
  urlstatus = true;
    } else {
      $(this).removeClass('cur');
    }
	if($("#zpfl_list a.cur").length>1){
	$("#zpfl_list a").eq(0).removeClass('cur');
	}
	});
}
//富媒体（右下角）
function fmta(){
document.writeln("<script src=\'//pc.weizhenwx.com/pc/rich-tf.js\' id=\'richid\' data=\'s=3631\'></script>");
}

//固定位
function gu831(){

}

//快应用代码（背投）
function kuai(){

}

//站长统计
function tongji(){
document.writeln("<script type=\'text/javascript\' src=\'https://s4.cnzz.com/z_stat.php?id=1278613071&web_id=1278613071\'></script>");
}