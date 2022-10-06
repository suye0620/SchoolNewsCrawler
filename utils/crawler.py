from time import sleep
from bs4 import BeautifulSoup
from tqdm import tqdm
from multiprocessing import Pool,Process
from math import floor
# from itertools import product
from functools import partial
import requests
import re
import pandas as pd

# 伪装的请求头
one_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
}

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
        self.save_path = ''

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

class HustCrawler:
    """
    爬取华科要闻的爬虫
    """
    def __init__(self,site:str,site_name:str,headers:dict):
        self.site = site
        self.site_name = site_name
        self.headers = headers
        self.list_to_visit = []
        self.page_num = 0
        self.save_path = ''

    def countPageNum(self):
        """
        :update page_num: 该站点需要翻页的次数,用于生成待爬取url
        """
        response = requests.get(self.site,headers=self.headers)
        status = response.status_code

        if status == 200:
            # 使用bs解析网页，获取要翻页的次数
            bs_site = BeautifulSoup(response.text,"html.parser")
            # self.page_num = int(bs_site.select("#fanye208414")[0].get_text())
            # 截取页数
            self.page_num = int(re.findall("/[1-9][0-9][0-9]",string=bs_site.select("#fanye208414")[0].get_text())[0][1:])
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
            temp = "http://news.hust.edu.cn/xxyw/{}.htm".format(i)
            # 休眠
            if i%10 == 0:
                sleep(5)
            
            # 首页
            if i == endpage:
                temp = "http://news.hust.edu.cn/xxyw.htm"

            try:
                response = requests.get(temp,headers=self.headers).content.decode()
                bs_onepage =  BeautifulSoup(response,"lxml")
                # list_urls = bs_onepage.find_all("span",attrs={'class':'Article_Title'})
                list_urls = bs_onepage.select('span.Article_Title > a')
                df = pd.DataFrame(columns=['link','title','site_name','pagenum',])
                for url in list_urls:
                    list_info = []
                    list_info.append('http://news.hust.edu.cn'+url.attrs['href'][2:])
                    list_info.append(url.attrs['title'])
                    list_info.append(self.site_name)
                    list_info.append(i)
                    # append方法要被废弃了，有点无语，暂时用下面的写法
                    df.loc[df.shape[0]] = list_info
                df.to_csv(urlsfile_path,encoding='utf-8-sig',index = False,mode='a',header=False)
            except requests.exceptions.RequestException:
                return None

def parse(url,headers:dict = one_header)->list:
    """
    :param url: 需要解析的一个页面
    :return article_content: 包含文章内容的所有tag的list
    """
    try:
        res = requests.get(url,headers=headers).content.decode()
        bs_onearticle = BeautifulSoup(res,'lxml')
        # article_content = bs_onearticle.select("div.wp_articlecontent > p")
        article_content = bs_onearticle.find_all(name="div",attrs={"class":"wp_articlecontent"})
        # article_content是一个列表，索引0取第一个，然后调用get_text方法
        # list_paragraphs = [p.get_text() for p in article_content].remove('')
        
        # return [p.get_text()+'\n' for p in list_paragraphs]
        return [article_content[0].get_text()]
    except requests.exceptions.RequestException as e:
        print(e)
    
def subCrawl(save_path:str, one_df:pd.DataFrame):
    """
    :param one_df: 对getUrls生成的df进行拆分后的小df,用于多进程处理
    """
    nrow = one_df.shape[0]
    for row in tqdm(range(nrow),desc='crawling...'):
        article_content = parse(one_df['link'][row])
        # 生成存储文件名
        txtfile_name = one_df['link'][row][26:-9].replace("/","_")+".txt"
        with open(file=(save_path+txtfile_name),mode='w',encoding='utf-8') as f:
            f.writelines(article_content)
        # 完成写入，关闭文件
        f.close()

def crawl(urlsfile_path:str,save_path:str,processes_num=8):
    """
    :param urlsfile_path: 存储待爬取网址的路径
    :param save_path: 存储爬取结果的路径
    :param processes_num: 单进程下普通单核cpu只能以20s/it的速度爬取解析.需开启多进程,该参数为进程数

    """
    df = pd.read_csv(urlsfile_path,encoding='utf-8-sig')
    nrow = df.shape[0]
    # 计算每一小份的数量
    every_epoch_num = floor((nrow/processes_num))

    # 对原始的df按照processes_num进行分组
    pool_dfs = []
    for index in tqdm(range(processes_num)):
        if index < processes_num-1:
            df_tem = df[every_epoch_num * index: every_epoch_num * (index + 1)]
        else:
            df_tem = df[every_epoch_num * index:]
        pool_dfs.append(df_tem.copy())

    # 传参冻结
    new_subCrawl = partial(subCrawl,save_path)
    # 创建进程池
    # pool = Pool(processes=processes_num)
    # for df in pool_dfs:
    #     pool.apply_async(new_subCrawl,args=(df,))
    # pool.close()
    # pool.join()

    list_processes = []
    for df in pool_dfs:
        p = Process(target=new_subCrawl,args=[df])
        p.start()
        list_processes.append(p)
    for p in list_processes:
        p.join()
        
        


    