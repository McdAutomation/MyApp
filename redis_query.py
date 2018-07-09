import redis

r = redis.Redis()
print(r.set('hi','there'))
print(r.get('hi'))