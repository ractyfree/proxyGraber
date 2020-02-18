from siteclass.SpysOne import SpysOne
from siteclass.FreeProxiesList import FreeProxiesList
from siteclass.FreeProxyCZ import FreeProxyCZ
from siteclass.ProxyScrape import ProxyScrape
from siteclass.SSLProxiesOrg import SSLProxiesOrg

from WorkerThread import WorkerThread, WorkerThreadPool
import requests
import datetime
import os







class ProxyChecker:
    def __init__(self, 
    proxies:list, # [ [ip, port] ]
    threads=10, 
    max_timeout=5, 
    testlink="https://www.google.com"):
        self.__proxies = proxies
        self.__threads = threads
        self.__proxies = proxies
        self.__max_timeout = max_timeout
        self.__testlink = testlink
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "referer": "https://www.google.com",
            "sec-fetch-site":"same-origin"}
        self.file = "proxies"


    def __test_proxy(self, proxy:str): #proxy 127.0.0.1:9999
        proxy = {"http": proxy,
                "https": proxy}
        try:
            r = requests.request("GET", self.__testlink, headers=self.headers, proxies=proxy, timeout=self.__max_timeout)
            if r.status_code == 200:
                print(proxy['http'])
                return True
        except:
            return False   

    def __testProxyThreaded(self, results, proxy:str):
        if self.__test_proxy(proxy):
            results.append(proxy)
        return True


    def writeToFile(self, lst):
        try:
            os.mkdir("proxies")
        except FileExistsError:
            pass

        now = datetime.datetime.now()
        f = open(file="proxies/{0}[{1}].txt".format(self.file, now.strftime("%Y-%m-%d_%H-%M-%S")), mode="w")
        for x in lst:
            f.write("{0}\n".format(x))
        f.close()


    def do(self):
        tpool = WorkerThreadPool()
        i = 0
        results = []
        
        while True:
            for x in range(0,int(self.__threads)):
                try:
                    proxy = self.__proxies.pop()
                    proxy = "{0}:{1}".format(proxy[0], proxy[1])

                    thread = WorkerThread(func=self.__testProxyThreaded, args=[results, proxy])
                    tpool.addThread(thread)
                    i += 1
                except IndexError:
                    pass
            
            tpool.isAllThreadsDone()
            print("Proxies left to check: {0}".format(len(self.__proxies)))
            if len(self.__proxies) == 0:
                break

        return results

        


if __name__ == '__main__':

    summlist = []
    sslproxorg = SSLProxiesOrg()
    summlist.extend(sslproxorg.do())

    proxscrape = ProxyScrape()
    summlist.extend(proxscrape.do())

    freepcz = FreeProxyCZ()
    summlist.extend(freepcz.do())

    freeplist = FreeProxiesList()
    summlist.extend(freeplist.do())

    #spys = SpysOne()
    #summlist.extend(spys.do())

    proxch = ProxyChecker(summlist, threads=50)
    ret = proxch.do()
    proxch.writeToFile(ret)
    print(len(ret))

    

   #writeFileValidate(parsed)
