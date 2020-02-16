from . import SpysOne



testlink = "https://www.google.com"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "referer": "https://www.google.com",
            "sec-fetch-site":"same-origin"}

def test_proxy(proxy):
    try:
        r = requests.request("GET", testlink, headers=headers, proxies=proxy, timeout=2)
        if r.status_code == 200:
            return True3
    except:
        return False

def writeFileValidate(lst, file='proxies.txt', ):
    for x in lst:
        f = open(file, "a")
        proxy = "{0}:{1}".format(x[0], x[1])

        proxydict = {
            "https": proxy,
            "http": proxy
        }
        if test_proxy(proxydict):
            print(proxy)
            f.write(proxy +  '\n')
    f.close()



if __name__ == '__main__':
    spys = SpysOne()
    parsed = spys.do()
    writeFileValidate(parsed)
