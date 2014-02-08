from functools import wraps, partial
import time
import os
import config
from config import cache_path, cache_type
PATH = os.path.dirname(__file__)

CACHE_TYPE = {
    "file": 'PickleCache',
    "redis": 'RedisCache',
    # "memcache" : "MemCache"

}


def name_to_class(s):  # da nome a oggetto corrispondente
    if s in globals().keys() and issubclass(globals()[s], SolidCache):
        return globals()[s]
    return None


class SolidCache(object):

    def __init__(self):
        pass

    def init(self, name):
        raise NotImplementedError()

    def get_cache(self):
        raise NotImplementedError()

    def set_cache(self, c):
        raise NotImplementedError()

    def get(self, k, r):
        raise NotImplementedError()

    def set(self, k, v):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

    def stats(self):
        raise NotImplementedError()

    def dimension(self):
        raise NotImplementedError()

    def keys(self):
        raise NotImplementedError()

    def split(self):  # butta meta' delle entry con una qualche policy
        raise NotImplementedError()


class RedisCache(SolidCache):
    redis = __import__('redis')

    cache = None
    cache_name = ""

    def __init__(self, name):
        self.cache = self.redis.Redis(host=config.redis_host, port=config.redis_port, db=config.redis_db)
        self.cache_name = "newinf:%s:" % name

    def get_cache(self):
        r = {}
        for k in self.cache.keys(self.cache_name+'*'):
            r[eval(k.replace(self.cache_name, ''))] = self.cache.get(k)
        return r

    def set_cache(self, c):
        for k in c.keys():
            self.cache.set(self.cache_name+k, c[k])

    def get(self, k, r):
        k = str(k)
        v = self.cache.get(self.cache_name+k)
        return eval(v) if self.cache.exists(self.cache_name+k) else r

    def set(self, k, v):
        k = str(k)
        self.cache.set(self.cache_name+k, v)

    def clear(self):
        self.cache.delete(self.cache_name+'*')

    def save(self):
        self.cache.bgsave()

    def stats(self):
        return {"cache_size": self.dimension(),
                "info": self.cache.info()}

    def dimension(self):
        return len(self.cache.keys(self.cache_name+'*'))

    def keys(self):
        return [eval(k.replace(self.cache_name, '')) for k in self.cache.keys(self.cache_name+'*')]

    def split(self):  # butta meta' delle entry con una qualche policy
        for k in self.cache.keys(self.cache_name+'*')[:self.dimension()/2]:
            self.cache.delete(str(k))


class PickleCache(SolidCache):
    # faccio l'import del modulo relativo nella classe in modo che serva solo se si usa quel tipo di cache
    pickle = __import__('pickle')

    cache = {}
    cache_path = ""
    cache_file = ""
    last_access = None
    cache_name = ""

    def __init__(self, name):

        self.cache_name = name
        self.cache_path = os.path.join(PATH, cache_path)
        self.cache_file = os.path.join(self.cache_path, name)  # sperabilmente il nome di funzione non contiene char
                                                               # speciali quindi ok per un file. (assunzione scema?)
        try:  # mi assicuro che la directory dove scrivero' esista e sia buona
            os.makedirs(self.cache_path)
        except OSError:
            if not os.path.isdir(self.cache_path) or not os.access(self.cache_path, os.W_OK):
                raise
        if os.path.isfile(self.cache_file):
            f = open(self.cache_file, 'rb')
            self.cache = self.pickle.load(f)
            f.close()
        else:
            f = open(self.cache_file, 'wb')
            self.pickle.dump(self.cache, f)
            f.close()

    def get_cache(self):
        return self.cache

    def set_cache(self, c):
        self.cache = c
        f = open(self.cache_file, 'wb')
        self.pickle.dump(self.cache, f)
        f.close()

    def get(self, k, r):
        return self.cache.get(k, r)

    def set(self, k, v):
        self.cache[k] = v
        self.save()  # TODO: da rivedere jhonny! (delayed write? ogni tot? dopo n update?)

    def clear(self):
        self.cache = {}
        f = open(self.cache_file, 'wb')
        self.pickle.dump(self.cache, f)
        f.close()

    def save(self):
        f = open(self.cache_file, 'wb')
        self.pickle.dump(self.cache, f)
        f.close()

    def stats(self):
        return {"cache_size": len(self.cache)-2,
                "cache_size_ondisk": os.path.getsize(self.cache_file),
                "created": time.ctime(os.path.getctime(self.cache_file)),
                "last_modify": time.ctime(os.path.getmtime(self.cache_file))}

    def dimension(self):
        return len(self.cache)

    def keys(self):
        return self.cache.keys()

    def split(self):
        badk = self.cache.keys()[:len(self.cache)/2]  # butto a merda meta' chiavi
        [self.cache.pop(k) for k in badk]


def select_cache(*args):
    ctype = CACHE_TYPE.get(cache_type, 'PickleCache')
    return name_to_class(ctype)(*args)


def cached_in(func=None, expire=60, maxsize=32):

    if func is None:
        return partial(cached_in, expire=expire, maxsize=maxsize)

    func.cache = select_cache(func.__name__)
    func.cache_expire = expire
    func.cache_hit = 0
    func.cache_miss = 0
    func.cache_filled = 0
    func.cache_maxsize = maxsize

    def cache_s():
        return {"hit": func.cache_hit,
                "miss": func.cache_miss,
                "maxsize": func.cache_maxsize,
                "actualsize": func.cache.dimension()}

    func.cache_stats = cache_s

    def cache_c():
        func.cache.clear()
        func.cache_hit = 0
        func.cache_miss = 0

    func.cache_clear = cache_c

    @wraps(func)
    def wrapper(*args):
        result = None
        when, cresult = func.cache.get(args, (None, None))
        if when is None and cresult is None:
            func.cache_miss += 1

            if func.cache.dimension() == func.cache_maxsize:
                func.cache_filled += 1
                func.cache.split()

            result = func(*args)
            func.cache.set(args, (time.time(), result))
        else:
            elapsed = time.time() - when
            if elapsed / 60 > func.cache_expire:
                func.cache_miss += 1
                result = func(*args)
                func.cache.set(args, (time.time(), result))
            else:
                func.cache_hit += 1
                result = cresult

        return result

    return wrapper