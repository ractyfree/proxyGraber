import requests
from lxml import html



class SSLProxiesOrg:
    """
    Parser for "https://www.sslproxies.org/"
    
    Methods
    -------
    do() -> list
        returns list of proxies from the site
    """
    def __init__(self):
        self.__baseLink = "https://www.sslproxies.org/"


    def do(self):
        page = requests.request("GET", self.__baseLink).text
        tree = html.fromstring(page)
        retlst = []
        for x in tree.xpath("//table[@class='table table-striped table-bordered']/tbody/tr"):
            retlst.append([x.xpath("td[1]")[0].text, x.xpath("td[2]")[0].text])
        return retlst
