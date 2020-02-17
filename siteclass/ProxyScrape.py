import requests
from lxml import html



class ProxyScrape:
    """
    Proxy parser for an API of https://proxyscrape.com/free-proxy-list

    Attributes
    -----
    proto : str //http, socks4, socks5
        defines a type of proxy to parse from the site
    
    timeout : int
        defines a timeout of proxies to parse in Milli

    country : str // all, US, RU, AM, ....
        defines a country to be used in parsing
    ssl : BOOLEAN // TRUE, FALSE, NONE
        defines an ssl protocol to be used in parsing

    annonymity : str // all, elite, anonymous, transparent
        defines a level of proxy's annonymity


    Methods
    -----
    do() -> list // [[ip, port], [ip, port]]
        Starts parsing

    """
    def __init__(self, 
                proto="http", 
                timeout=10000, 
                country="all", 
                ssl=True, 
                anonymity="all"):
        #&proxytype=http&timeout=10000&country=all&ssl=yes&anonymity=all
        self.__baseLink = "https://api.proxyscrape.com/?request=getproxies"
        self.proto = proto
        self.timeout = str(timeout)
        self.country = country
        self.ssl = "yes" if ssl else ("no" if not ssl else "all")
        self.anonymity = anonymity

    def __builderLink(self):
        return "{0}&proxytype={1}&timeout={2}&country={3}&ssl={4}&anonymity={5}".format(
        self.__baseLink, 
        self.proto, 
        self.timeout,
        self.country,
        self.ssl,
        self.anonymity
        )

    def __parseResp(self, resp):
        return [x.split(":") for x in resp.split("\r\n")]

    def do(self):
        link = self.__builderLink()
        resp = requests.request("GET", link).text
        return self.__parseResp(resp)


if __name__ == "__main__":
    prox = ProxyScrape()
    prox.do()
