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

    def countPageNum(self)->int:
        """
        :update page_num: 该站点需要翻页的次数,用于生成待爬取url
        """
        response = requests.get(self.site,headers=self.headers)
        status = response.status_code

        if status == 200:
            # 使用bs解析网页，获取要翻页的次数
            bs_site = BeautifulSoup(response.text,"html.parser")
            self.page_num = bs_site.find(name='em',attrs={'class':'all_pages'}).get_text()
            # print(self.page_num)
            return int(self.page_num)
        else:
            print("访问站点遇到了问题")
    
    def getUrls(self,startpage:int,endpage:int):
        """
        :param startpage:要获取链接的第一页
        :param endpage:要获取链接的最后一页
        :update list_to_visit: 获取所有页上新闻的url链接,存入list_to_visit
        """
        for i in range(startpage,endpage+1):
            temp = "http://wellan.zuel.edu.cn/1668/list{}.htm".format(i)
            try:
                response = requests.get(temp,headers=self.headers).content.decode()
                bs_onepage =  BeautifulSoup(response,"lxml")
                # list_urls = bs_onepage.find_all("span",attrs={'class':'Article_Title'})
                list_urls = bs_onepage.select('ul > li.list_item > div.fields.pr_fields > span.Article_Title > a')
                df = pd.DataFrame(columns=['link','title','site_name','pagenum',])
                for url in list_urls:
                    list_info = []
                    list_info.append('http://wellan.zuel.edu.cn'+url.attrs['href'])
                    list_info.append(url.attrs['title'])
                    list_info.append(self.site_name)
                    list_info.append(i)
                    # append方法要被废弃了，有点无语，暂时用下面的写法
                    df.loc[df.shape[0]] = list_info
                df.to_csv("./data/urls.csv",encoding='utf-8-sig',index = False,mode='a')
            except requests.exceptions.RequestException:
                return None

    def parse(self,url):
        """
        :param url: 需要解析的一个页面
        :return article_content: 文章内容
        """
        try:
            res = requests.get(url,headers=self.headers).content.decode()
            bs_onearticle = BeautifulSoup(res,'lxml')
            
        except requests.exceptions.RequestException as e:
            print(e)


    