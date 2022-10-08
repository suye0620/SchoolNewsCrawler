from utils.crawler import ZuelCrawler,crawlZuel,one_header,HustCrawler,crawlHust

if __name__ == "__main__":
    
    # 文澜要闻
    # zuelCrawler_1668 = ZuelCrawler("http://wellan.zuel.edu.cn/1668/list.htm","文澜要闻",headers = one_header)
    
    # 数要翻页的次数
    # print("查询页数中...")
    # zuelCrawler_1668.countPageNum()
    # print(zuelCrawler_1668.getPageNum())
    
    # 获取要爬取的url
    # print("翻页中...")
    # zuelCrawler_1668.getUrls(startpage = 1,endpage = zuelCrawler_1668.getPageNum(),urlsfile_path="./data/zuelurls-文澜要闻.csv")

    # 华科学校要闻
    # HustCrawler_xxyw = HustCrawler("http://news.hust.edu.cn/xxyw.htm","华科学校要闻",headers = one_header)
    
    # 数要翻页的次数
    # print("查询页数中...")
    # HustCrawler_xxyw.countPageNum()
    # print(HustCrawler_xxyw.getPageNum())
    
    # 获取要爬取的url
    # print("翻页中...")
    # HustCrawler_xxyw.getUrls(startpage = 1,endpage = HustCrawler_xxyw.getPageNum(),urlsfile_path="./data/husturls-学校要闻.csv")
    
    # 测试parse函数
    # zuelCrawler_1668.parse(url='http://wellan.zuel.edu.cn/2022/0921/c1668a306614/page.htm')
    
    # 爬取
    print("爬取中...")
    # zuel
    # crawlZuel(urlsfile_path="./data/zuelurls-文澜要闻.csv",save_path="./data/zuel_news/文澜要闻/",startrow=1400)
    # hust
    crawlHust(urlsfile_path="./data/husturls-学校要闻.csv",save_path="./data/hust_news/学校要闻/",startrow=270)
    # zuelCrawler_1668.crawl(urlsfile_path="./data/urls.csv",save_path="./data/zuel_news/")

