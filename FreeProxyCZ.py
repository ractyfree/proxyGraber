import requests
import cloudscraper
import base64
import re
from lxml import html


class FreeProxyCZ:
    """
    FreeProxyCZ parser
    uses cloudparser to bypass cloudflare

    Attributes
    ----------
    countries : list
        countries list to parse
    proto : str // HTTPS, HTTP, Socks4/5, Socks4, Socks5
        protos to be used in parsing
    anonymity : str // LEVEL1, LEVEL2, LEVEL3
        anonymity level of proxies

    Methods
    ---------
    do() -> list
        Main routine
    """
    def __init__(self, countries=None, proto="HTTPS", anonymity=None):
        self.__baseLink = "http://free-proxy.cz/ru"
        self.__scraper = cloudscraper.create_scraper() #get/post
        self.__countries = countries if countries else 'all'
        self.__proto = proto.lower() if proto else 'all'
        self.__anonymity = anonymity.replace(" ", "") if anonymity else 'all'

    def __initBuilderLinks(self):
        if self.__countries and type(self.__countries) == list:
            return ["{0}/proxylist/country/{1}/{2}/ping/{3}".format(self.__baseLink, x, self.__proto, self.__anonymity) for x in self.__countries]
        else:
            return "{0}/proxylist/country/{1}/{2}/ping/{3}".format(self.__baseLink, self.__countries, self.__proto, self.__anonymity)

    def __parseIp(self, _str):
        return re.search(r'([\'\"])(.*)\1', _str).group(2)

    def do(self):
        link = self.__initBuilderLinks() # //i

        page = self.__scraper.get(link).text
        tree = html.fromstring(page)
        cntpages =  int(tree.xpath("//div[@class='paginator']/a")[-2].text)

        retlst = []
        for x in range(1, cntpages+1):
            page = self.__scraper.get("{0}/{1}".format(link, x)).text
            tree = html.fromstring(page)

            for x in tree.xpath("//table[@id='proxy_list']/tbody/tr"):
                try:
                    ip = base64.b64decode(self.__parseIp(x.xpath("td[@style='text-align:center']/script[@type='text/javascript']")[0].text)).decode("utf-8")
                    port = x.xpath("td/span[@class='fport']")[0].text
                    #proto = x.xpath("td/small")[0].text
                    retlst.append([ip, port])
                except:
                    pass
        return retlst