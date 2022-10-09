from time import sleep
from tqdm import tqdm
import re
import pandas as pd
from selenium import webdriver

web_option = webdriver.FirefoxOptions()
web_option.add_argument('--headless')
web_option.add_argument('--disable-gpu')
web_option.add_argument('window-size=1200x600')
web_option.add_argument('--blink-settings=imagesEnabled=false')
web_option.set_capability("pageLoadStrategy", "eager")

# 伪装的请求头
one_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
}

# 创建一个webdriver
def createWebdriver(options = web_option,executable_path = './utils/geckodriver.exe'):
    """
    :param options: webdriver的配置
    :param executable_path: 驱动器的存放路径
    :return webdriver: Firefox
    """
    return webdriver.Firefox(options=options,executable_path=executable_path,log_path="./log/")

class ZuelCrawler:
    """
    爬取文澜新闻网综合新闻的爬虫
    """
    def __init__(self,site:str,site_name:str,headers:dict):
        self.site = site
        self.site_name = site_name
        self.headers = headers
        self.list_to_visit = []
        self.page_num = 0

    def countPageNum(self,mywebdriver):
        """
        :update page_num: 该站点需要翻页的次数,用于生成待爬取url
        """
        mywebdriver.get(self.site)
        self.page_num = int(mywebdriver.find_element(by='css selector',value='em.all_pages').text)

    def getPageNum(self)->int:
        return self.page_num
    
    def getUrls(self,mywebdriver,startpage:int,endpage:int,urlsfile_path:str,):
        """
        :param startpage: 要获取链接的第一页
        :param endpage: 要获取链接的最后一页
        :update list_to_visit: 获取所有页上新闻的url链接,存入list_to_visit
        """
        for i in tqdm(range(startpage,endpage+1),desc='getUrls:'):
            # 如果还要爬其他板块就修改1669,后面可放出接口
            temp = "http://wellan.zuel.edu.cn/1669/list{}.htm".format(i)
            if i%10 == 0:
                sleep(5)
            mywebdriver.get(temp)
            list_urls = mywebdriver.find_elements(by='css selector',value='ul > li.list_item > div.fields.pr_fields > span.Article_Title > a')
            df = pd.DataFrame(columns=['link','title','site_name','pagenum',])
            for url in list_urls:
                list_info = []
                list_info.append(url.get_attribute('href'))
                list_info.append(url.get_attribute('title'))
                list_info.append(self.site_name)
                list_info.append(i)
                # append方法要被废弃了，有点无语，暂时用下面的写法
                df.loc[df.shape[0]] = list_info
            df.to_csv(urlsfile_path,encoding='utf-8-sig',index = False,mode='a')
        
class HustCrawler:
    """
    爬取华科综合新闻的爬虫
    """
    def __init__(self,site:str,site_name:str,headers:dict):
        self.site = site
        self.site_name = site_name
        self.headers = headers
        self.list_to_visit = []
        self.page_num = 0
        self.webdriver = createWebdriver()

    def countPageNum(self):
        """
        :update page_num: 该站点需要翻页的次数,用于生成待爬取url
        """
        self.webdriver.get(self.site)
        self.page_num = int(re.findall("/[1-9][0-9][0-9]",string=self.webdriver.find_element(by='css selector',value='#fanye208414').text)[0][1:])

    def getPageNum(self)->int:
        return self.page_num
    
    def getUrls(self,startpage:int,endpage:int,urlsfile_path:str):
        """
        :param startpage: 要获取链接的第一页
        :param endpage: 要获取链接的最后一页
        :update list_to_visit: 获取所有页上新闻的url链接,存入list_to_visit
        """
        for i in tqdm(range(endpage,startpage,-1),desc='getUrls:'):
            temp = "http://news.hust.edu.cn/zhxw/{}.htm".format(i)
            # 首页
            if i == endpage:
                temp = "http://news.hust.edu.cn/zhxw.htm"
            # 休眠
            if i%10 == 0:
                sleep(5)

            try:
                self.webdriver.get(temp)
                list_urls = self.webdriver.find_elements(by='css selector',value='span.Article_Title > a')
                df = pd.DataFrame(columns=['link','title','site_name','pagenum',])
                for url in list_urls:
                    list_info = []
                    list_info.append(url.get_attribute('href'))
                    list_info.append(url.get_attribute('title'))
                    list_info.append(self.site_name)
                    list_info.append(i)
                    # append方法要被废弃了，有点无语，暂时用下面的写法
                    df.loc[df.shape[0]] = list_info
                df.to_csv(urlsfile_path,encoding='utf-8-sig',index = False,mode='a',header=False)
            except:
                return None
        
def crawlZuel(urlsfile_path:str,save_path:str,startrow:int=0):
    """
    :param urlsfile_path: 存储待爬取网址的路径
    :param save_path: 存储爬取结果的路径
    :param webdrivers_num: 单进程下使用request,普通单核cpu只能以20s/it的速度爬取解析.故考虑使用selenium,开启多个webdriver
    """
    df = pd.read_csv(urlsfile_path,encoding='utf-8-sig')
    nrow = df.shape[0]
    mywebdriver = createWebdriver()
    for row in tqdm(range(startrow,nrow),desc='crawling...'):
        # 访问
        mywebdriver.get(df['link'][row])
        article_content = mywebdriver.find_elements(by='css selector',value='div.wp_articlecontent')[0].text
        # 生成存储文件名
        txtfile_name = df['link'][row][26:-9].replace("/","_")+".txt"

        # 写入
        with open(file=(save_path+txtfile_name),mode='w',encoding='utf-8') as f:
            # 写入标题
            f.write(df['title'][row]+'\n')
            # 写入内容
            f.write(article_content)
        # 完成写入，关闭文件
        f.close()
        sleep(0.5)
    mywebdriver.close()

def crawlHust(urlsfile_path:str,save_path:str,startrow:int=0,webdrivers_num=3):
    """
    :param urlsfile_path: 存储待爬取网址的路径
    :param save_path: 存储爬取结果的路径
    :param webdrivers_num: 单进程下使用request,普通单核cpu只能以20s/it的速度爬取解析.故考虑使用selenium,开启多个webdriver
    """
    df = pd.read_csv(urlsfile_path,encoding='utf-8-sig')
    nrow = df.shape[0]
    mywebdriver = createWebdriver()
    for row in tqdm(range(startrow,nrow),desc='crawling...'):
        # 访问
        mywebdriver.get(df['link'][row])
        # WebDriverWait(driver = mywebdriver,timeout=5 ).until(EC.presence_of_element_located((By.CSS_SELECTOR,'h1.arti_title')))
        article_content = mywebdriver.find_elements(by='css selector',value='div.v_news_content')[0].text
        
        # 生成存储文件名
        txtfile_name = df['link'][row][29:-4].replace("/","_")+".txt"

        # 写入
        with open(file=(save_path+txtfile_name),mode='w',encoding='utf-8') as f:
            # 写入标题
            f.write(df['title'][row]+'\n')
            # 写入内容
            f.write(article_content)
        # 完成写入，关闭文件
        f.close()
        sleep(3)
    mywebdriver.close()
    