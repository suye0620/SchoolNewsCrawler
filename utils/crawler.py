import requests
from bs4 import BeautifulSoup
import pandas as pd

class zuelCrawler:
    """
    爬取文澜新闻网的爬虫
    """
    def __init__(self,site:str,site_name:str,headers:dict):
        self.site = site
        self.site_name = site_name
        self.headers = headers
        self.list_to_visit = []
        self.page_num = 0

    def countPageNum(self):
        """
        :update page_num: 该站点需要翻页的次数,用于生成待爬取url
        """
        response = requests.get(self.site,headers=self.headers)
        status = response.status_code

        if status == 200:
            # 使用bs解析网页，获取要翻页的次数
            bs_site = BeautifulSoup(response.text,"html.parser")
            self.page_num = bs_site.find(name='em',attrs={'class':'all_pages'}).get_text()
            print(self.page_num)
        else:
            print("访问站点遇到了问题")
    
    def getUrls(self,startpage:int,endpage:int):
        """
        :param startpage:要获取链接的第一页
        :param endpage:要获取链接的最后一页
        :update list_to_visit: 获取所有页上新闻的url链接,存入list_to_visit
        """
        for i in range(startpage,endpage+1):
            temp = "http://wellan.zuel.edu.cn/1668/list{}.htm".format(i+1)
            try:
                response = requests.get(temp,headers=self.headers)
                bs_onepage =  BeautifulSoup(response,"html.parser")

            except requests.exceptions.RequestException:
                return None
            


    