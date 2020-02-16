import requests
from lxml import html
import time


class ProxyParser():
   
    @staticmethod
    def getPage(link, headers=None, data=None, proxies=None, timeout=None, reqtype="GET"):
        print(link)
        return requests.request(reqtype, link, headers=headers, data=data, proxies=proxies, timeout=timeout).text

    


    


class SpysOne(ProxyParser):
    """
    SpysOne proxy parser.

    Attributes
    ----------
    countries : list
        list of countries to parse
    _type : str
        type of proxies to parse e.g SOCKS/HTTP/All
    cntpage : int
        count of proxies to display on the page

    Methods
    ------
    do() -> list
        Start parsing process. Returns the list of proxies formated: [['ip', 'port'], ['ip', 'port'], ['ip', 'port'], ...]

    """
    def __init__(self, countries=["RU", "US"], _type="HTTP", cntpage=500):
        
        self.__baselink = "http://spys.one/free-proxy-list/"
        self.__countries=countries
        self.__cntpage = cntpage
        self.__type = _type
        self.__sel = SeleniumWrapper()

        self.__cntdict = {
            30: '0',
            50: '1',
            100: '2',
            200: '3',
            300: '4',
            500: '5'}

        self.__typedict = {
            'HTTP': '1',
            'All': '0',
            'SOCKS': '2'
        }



    def __parsePage(self, page):
        tree = html.fromstring(page)
        lst = tree.xpath("//tr[@class='spy1xx']/td[1]/font[@class='spy14']/text()")
        n = 2
        return [lst[i * n:(i + 1) * n] for i in range((len(lst) + n - 1) // n )]  



    def __waitPageLoaded(self):
        self.__sel.waitPageLoaded("//meta[@name='description']")

    def __clickSelection(self, selection):
        for x in range(3):
            self.__sel.click(selection)
            self.__waitPageLoaded()

            if self.__sel.getElementByXPATH(selection).get_attribute('selected'):
                break

    def do(self):
        retlst = []
        for x in self.__countries:
            self.__sel.openPage("{0}{1}".format(self.__baselink, x))

            self.__sel.waitPageLoaded("//meta[@name='description']")

            if self.__type:
                self.__clickSelection("//select[@name='xf5']/option[@value='{0}']".format(self.__typedict[self.__type]))

            if self.__cntpage:
                self.__clickSelection("//select[@name='xpp']/option[@value='{0}']".format(self.__cntdict[self.__cntpage]))

            retlst.extend(self.__parsePage(self.__sel.getCurrentPage()))
        self.__sel.close()

        return retlst

