__author__ = 'mandrake'

########### GLOBAL
#host = 'localhost'
host = '0.0.0.0'
port = 5000
debug = True
cache_path = ".cache"
cache_type = "redis"

########## REDIS
# se serve etc etc
redis_host = "localhost"
redis_port = 6379
redis_db = 0


########## API
api_version = 0.1

########## TWISTED/WSGI
twisted_pool_max = 500
twisted_pool_suggested = 20