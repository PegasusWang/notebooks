#!/usr/bin/env python
# -*- coding:utf-8 -*-


def application(environ, start_response):
    # print(environ)
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf8')]

    query_string = environ['QUERY_STRING']    # 这里是 "name=John"
    name = query_string.split("=")[1]    # 从查询字符串 "name=John" 里获取 "John"
    start_response(status, headers)
    return [b"<h1>Hello, {}!</h1>".format(name)]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('127.0.0.1', 8000, application)
    httpd.serve_forever()
