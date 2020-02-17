import requests
from lxml import html


class FreeProxiesList:
     """
        Parser for "https://free-proxy-list.net/"
        
        Attributes:
        HTTPS : BOOLEAN
            determines which type of proxies to parse from the site


        Methods
        -------
        do() -> list
            returns list of proxies from the site
    """
    def __init__(self, HTTPS=True):
        self.__baseLink = "https://free-proxy-list.net/"
        self.__HTTPS = HTTPS


    def do(self):
        page = requests.request("GET", self.__baseLink).text
        tree = html.fromstring(page)
        retlst = []
        for x in tree.xpath("//table[@class='table table-striped table-bordered']/tbody/tr"):
            if self.__HTTPS:
                if x.xpath("td[@class='hx']")[0].text == "yes":
                    retlst.append([x.xpath("td[1]")[0].text, x.xpath("td[2]")[0].text])
            else:
                retlst.append([x.xpath("td[1]")[0].text, x.xpath("td[2]")[0].text])
        return retlst