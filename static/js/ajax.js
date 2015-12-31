
function doAjax(id,url)
{
	//创建xmlhttp对象
	var xmlhttp=null;
	//IE7.0及以上版本和FIREFOX等浏览器
	if(window.XMLHttpRequest)
	{
		xmlhttp=new XMLHttpRequest();
	}
	//IE6.0及之前的IE版本
	else
	{
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	//时间戳
	var index=url.indexOf("?");
	if(index!=-1)
	{
		url+="&";
	}
	else
	{
		url+="?";
	}
	url+="time="+new Date().getTime();
	
	
	//打开异步请求 第一个参数是提交的方式 第二个参数表示提交的URL 第三个参数表示是否以异步方式请求
	xmlhttp.open("get", url, true);
	//发送请求
	xmlhttp.send(null);
	
	//异步请求响应状态事件
	xmlhttp.onreadystatechange=function()
	{
		//如果请求已被处理并响应完成
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			var div=document.getElementById(id);
			//将xmlhttp对象请求得到的结果呈现在页面中
			div.innerHTML=xmlhttp.responseText;
			//alert(xmlhttp.responseText);
		}
	}
	
//	xmlHttp.readyState		  
//	0: 请求未初始化 
//	1: 服务器连接已建立 
//	2: 请求已接收 
//	3: 请求处理中 
//	4: 请求已完成，且响应已就绪 

//	xmlHttp.states
//	200: "OK"
//	404: 未找到页面
	
	//alert("success");
	
}
