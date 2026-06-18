import string

BASE62 = string.digits + string.ascii_letters # 0-9, a-z, A-Z

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]
    result = ""
    while num > 0:
        result = BASE62[num % 62] + result
        num //= 62
    return result
    