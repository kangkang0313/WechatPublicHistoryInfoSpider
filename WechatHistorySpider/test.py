# -*- encoding:utf-8 -*-
from urllib import parse
import urllib.request
# params = parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})

params_ = parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})   ###自动转化成下面url的参数形式
params = 'eggs=2&bacon=0&spam=1'

# f = urllib.request.urlopen("http://www.musi-cal.com/cgi-bin/query?%s" % params)
# print (f.read())

a = parse.quote('张三')
http = 'http://www.baidu.com/s?name={}'.format(a)
print(http)
b='%E2%80%9C%E8%AD%A6%E7%A4%BA%E2%80%9D%E6%B4%BB%E5%8A%A8%E8%8E%B7%E5%A5%96%E5%90%8D%E5%8D%95%EF%BC%8C%E9%A2%86%E5%8F%96%E5%A4%A7%E5%A5%96%E5%9B%9E%E5%AE%B6%E8%BF%87%E5%B9%B4%EF%BC%81%EF%BC%81%EF%BC%81'
c = parse.unquote(b)
print(c)