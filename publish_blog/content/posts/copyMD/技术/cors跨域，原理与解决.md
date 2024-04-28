---
title: cors跨域，原理与解决
top: false
cover: false
toc: true
mathjax: true
date: 2023-08-1 15:27:31
password:
summary:
tags:
- web api
- cgi
categories:
- 综合
---



# 背景

需求：目前我需要在浏览器实现跨域请求访问我的服务。但是由于浏览器同源策略，导致访问不了。

思路：在服务器端设置允许跨域请求。

以前我只注意到了简单请求的跨域问题，没有注意到复杂请求的跨域问题，这篇文章着重解决一下。



# 请求分类

浏览器将CORS请求分成两类：简单请求（simple request）和非简单请求（not-so-simple request）。

只要同时满足以下两大条件，就属于简单请求。
```
浏览器将CORS请求分成两类：简单请求（simple request）和非简单请求（not-so-simple request）。

只要同时满足以下两大条件，就属于简单请求。

（1) 请求方法是以下三种方法之一：
    HEAD
    GET
    POST
（2）HTTP的头信息不超出以下几种字段：
    Accept
    Accept-Language
    Content-Language
    Last-Event-ID
    Content-Type：只限于三个值application/x-www-form-urlencoded、multipart/form-data、text/plain
```



# 简单请求

对于简单请求，浏览器直接发出CORS请求。具体来说，**就是在头信息（header）之中，增加一个`Origin`字段。**

下面是一个例子，浏览器发现这次跨源AJAX请求是简单请求，就自动在头信息之中，添加一个`Origin`字段。

```

GET /cors HTTP/1.1
Origin: http://api.bob.com
Host: api.alice.com
Accept-Language: en-US
Connection: keep-alive
User-Agent: Mozilla/5.0...
```

对于简单请求，服务器端直接放行即可。

在flask里面就是添加

`    CORS(app, supports_credentials=True, resources={r"/*": {"origins": '0.0.0.0'}})`

如果`Origin`指定的域名在许可范围内，服务器返回的响应，会多出几个头信息字段。

> ```http
> Access-Control-Allow-Origin: http://api.bob.com
> Access-Control-Allow-Credentials: true
> Access-Control-Expose-Headers: FooBar
> Content-Type: text/html; charset=utf-8
> ```



# 非简单请求

非简单请求的CORS请求，会在正式通信之前，增加一次HTTP查询请求，称为"预检"请求（preflight）。

浏览器先询问服务器，当前网页所在的域名是否在服务器的许可名单之中，以及可以使用哪些HTTP动词和头信息字段。只有得到肯定答复，浏览器才会发出正式的`XMLHttpRequest`请求，否则就报错。

下面是一段浏览器的JavaScript脚本。

> ```javascript
> var url = 'http://api.alice.com/cors';
> var xhr = new XMLHttpRequest();
> xhr.open('PUT', url, true);
> xhr.setRequestHeader('X-Custom-Header', 'value');
> xhr.send();
> ```



## OPTION预检

浏览器发现，这是一个非简单请求，就自动发出一个"预检"请求，要求服务器确认可以这样请求。下面是这个"预检"请求的HTTP头信息。

> ```http
> OPTIONS /cors HTTP/1.1
> Origin: http://api.bob.com
> Access-Control-Request-Method: PUT
> Access-Control-Request-Headers: X-Custom-Header
> Host: api.alice.com
> Accept-Language: en-US
> Connection: keep-alive
> User-Agent: Mozilla/5.0...
> ```

"预检"请求用的请求方法是`OPTIONS`，表示这个请求是用来询问的。头信息里面，关键字段是`Origin`，表示请求来自哪个源。

除了`Origin`字段，"预检"请求的头信息包括两个特殊字段。

**服务器回应的其他CORS相关字段如下**。

> ```http
> Access-Control-Allow-Methods: GET, POST, PUT
> Access-Control-Allow-Headers: X-Custom-Header
> Access-Control-Allow-Credentials: true
> Access-Control-Max-Age: 1728000
> ```



## 预检成功后

一旦服务器通过了"预检"请求，**以后每次浏览器正常的CORS请求，就都跟简单请求一样**，会有一个`Origin`头信息字段。服务器的回应，也都会有一个`Access-Control-Allow-Origin`头信息字段。

预检只需要一次即可，**但是无论是OPTIONS还是POST都必须要有必要的请求头**



## flask样例

```


# 接口返回格式 {"access_token":"gho_COSr3lUITUX9b2J7krsKjNlnlNSOBw2g0oZ1","token_type":"bearer","scope":"public_repo"}
@tool_blue.route('/get_access_token', methods=['POST', 'OPTIONS'])
def get_access_token():
    if request.method == 'OPTIONS':
        resp = make_response({})
        # 2、headers 中进行设置
        resp.headers["Content-Type"] = "application/json;chartset=UTF-8"  # 设置响应头
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'  # 如果有其它方法（delete,put等），断续添加
        resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return resp
    
    
    conf = get_config()
    client_id = conf["github"]["oauthApp"]["client_id"]
    client_secret = conf["github"]["oauthApp"]["client_secret"]
    code = request.json['code']
    url = 'https://github.com/login/oauth/access_token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code
    }
    headers = {
        'accept': 'application/json'
    }
    result = requests.post(url=url, params=params, headers=headers, verify=False)
    print(result.text)
    print(result.json())
    resp = make_response(result.json())

    # 2、headers 中进行设置
    resp.headers["Content-Type"] = "application/json;chartset=UTF-8"  # 设置响应头
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'  # 如果有其它方法（delete,put等），断续添加
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


# 不可以分成两个函数编写，否则会出现跨域问题，需要在同一个函数中进行处理
# @tool_blue.route('/get_access_token', methods=['OPTIONS'])
# def get_access_token_cors_option():
#     data = request.headers()
#     print(data)
#     resp = make_response(data)

#     # 2、headers 中进行设置
#     resp.headers["Content-Type"] = "application/json;chartset=UTF-8"  # 设置响应头
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'  # 如果有其它方法（delete,put等），断续添加
#     resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
#     return resp



```







# ref

[阮一峰](https://www.ruanyifeng.com/blog/2016/04/cors.html)

[你知道为何跨域中会发送 options 请求？](https://juejin.cn/post/7021077647417409550)

