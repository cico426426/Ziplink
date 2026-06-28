from abc import ABC, abstractmethod
import os
import redis
import time
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    db=int(os.getenv("REDIS_DB", "0")),
    decode_responses=True,
)

class RateLimiter(ABC):
    @abstractmethod
    def is_allowed(self, identifier: str) -> bool:
        pass

class TokenBucketLimiter(RateLimiter):
    def __init__(self, capacity: int = 5, refill_per_sec: float = 1.0):
        self.capacity = capacity
        self.refill_rate = refill_per_sec
    
    def is_allowed(self, identifier) -> bool:
        key = f"token_bucket:{identifier}"
        now = time.time()

        # https://redis.io/docs/latest/commands/hgetall/
        # Returns all fields and values of the hash stored at key. 
        bucket = r.hgetall(key)

        if not bucket:
            tokens = self.capacity
            last_refill = now
        else:
            tokens = float(bucket["tokens"])
            last_refill = float(bucket["last_refill"])
            elapsed = now - last_refill
            tokens = min(self.capacity, tokens + self.refill_rate * elapsed)

        allowed = tokens >= 1
        if allowed:
            tokens -= 1

        # https://redis.io/docs/latest/commands/hset/
        # Sets the specified fields to their respective values in the hash stored at key.
        r.hset(name=key, mapping={"tokens": tokens, "last_refill": now})
        r.expire(key, 3600)

        return allowed
    
class SlidingWindowLogLimiter(RateLimiter):
    def __init__(self, limit: int=5, window_seconds: int=60):
        self.limit = limit
        self.window_seconds = window_seconds

    def is_allowed(self, identifier) -> bool:
        key = f"sliding_window_log:{identifier}"
        now = time.time()
        
        # zremrangebyscore(清理 set 內部的成員)
        # 刪掉的是 sorted set 裡面那些過期的時間戳。一個還在活躍的使用者,他的 key 一直存在,但裡面會混著新舊時間戳——你必須把舊的清掉,才能正確計算「最近 60 秒內」有幾筆。這是每次請求都要做的,因為窗口一直在往前移動。
        # expire(清理整個 key)
        # 設定的是整個 key 多久後消失。針對的是不再來的使用者——如果一個 IP 從此不再請求,他的整個 key 會在 60 秒後自動消失,不會永遠佔著 Redis 記憶體。

        window_start = now - self.window_seconds
        
        # https://redis.io/docs/latest/commands/zremrangebyscore/
        # Removes all elements in the sorted set stored at key with a score between min and max (inclusive).
        r.zremrangebyscore(key, 0, window_start)
        
        # https://redis.io/docs/latest/commands/zcard/
        #Returns the sorted set cardinality (number of elements) of the sorted set stored at key.
        count = r.zcard(key)

        if count >= self.limit:
            return False
        
        r.zadd(key, {str(now): now})
        r.expire(key, self.window_seconds)
        return True
