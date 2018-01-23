import hashlib

def get_md5(url):
    if isinstance(url, str):     #如果是unicode则转换为utf-8编码
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# if __name__ == "__main__":        #测试get_md5
#     print(get_md5("http://jobbole.com".encode("utf-8")))