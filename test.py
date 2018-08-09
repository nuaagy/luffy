# import requests
#
# requests.post(
#     url='http://127.0.0.1:8888/api/post',
#     json={'a': 1, 'b': 2}
# )

from django.http import HttpRequest
# import redis, json
#
# conn = redis.Redis(host='192.168.11.169', port=6379)
# conn.hset('vip', 'name', {'x': 1})  # b"{'x': 1}"
# # conn.hset('vip', 'name', json.dumps({'x': 1}))  # b'{"x": 1}'
#
# v = conn.keys()
# print(conn.hgetall('vip'))
# a = conn.hget('vip', 'name')
# print(type(json.loads(a)))
# # conn.hset()
# b"{'x': 1}"


import redis, json

conn = redis.Redis(host='192.168.11.169', port=6379)
# conn.hset('x', 'y', {'z': 1})  # b"{'z': 1}"
conn.hset('x', 'y', json.dumps({'z': 1}))  # b'{"z": 1}'

d = conn.hget('x', 'y')
print(d)
# print(type(json.loads(d)))  # JSON 字符串 双引号json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
