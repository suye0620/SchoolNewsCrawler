from time import sleep
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

class ZuelCrawler:
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
            self.page_num = int(bs_site.select("em.all_pages")[0].get_text())
        else:
            print("访问站点遇到了问题")
    
    def getPageNum(self)->int:
        return self.page_num
    
    def getUrls(self,startpage:int,endpage:int,urlsfile_path:str):
        """
        :param startpage:要获取链接的第一页
        :param endpage:要获取链接的最后一页
        :update list_to_visit: 获取所有页上新闻的url链接,存入list_to_visit
        """
        for i in tqdm(range(startpage,endpage+1),desc='getUrls:'):
            temp = "http://wellan.zuel.edu.cn/1668/list{}.htm".format(i)
            if i%10 == 0:
                sleep(5)
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
                df.to_csv(urlsfile_path,encoding='utf-8-sig',index = False,mode='a')
            except requests.exceptions.RequestException:
                return None

    def parse(self,url)->list:
        """
        :param url: 需要解析的一个页面
        :return article_content: 包含文章内容的所有tag的list
        """
        try:
            res = requests.get(url,headers=self.headers).content.decode()
            bs_onearticle = BeautifulSoup(res,'lxml')
            article_content = bs_onearticle.select("div.wp_articlecontent > p")
            # article_content是一个列表，索引0取第一个，然后调用get_text方法
            return [p.get_text()+'\n' for p in article_content if p.get_text() != '']
        except requests.exceptions.RequestException as e:
            print(e)

    def crawl(self,urlsfile_path:str,save_path:str):
        """
        :param urlsfile_path: 需要爬取的网址文件
        """
        df = pd.read_csv(urlsfile_path,encoding='utf-8-sig')
        nrow = df.shape[0]
        for row in tqdm(range(nrow),desc='crawling...'):
            article_content = self.parse(df['link'][row])
            # 生成存储文件名
            txtfile_name = df['link'][row][26:-9].replace("/","_")+".txt"
            with open(file=(save_path+txtfile_name),mode='w',encoding='utf-8') as f:
                f.writelines(article_content)
            # 完成写入，关闭文件
            f.close()
            # if row%11 == 0:
            #     sleep(5)
        


    