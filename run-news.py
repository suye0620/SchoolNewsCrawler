from utils.crawler import ZuelCrawler,crawlZuel,one_header,HustCrawler,crawlHust

if __name__ == "__main__":
    
    # zuel-综合新闻
    zuelCrawler_1669 = ZuelCrawler("http://wellan.zuel.edu.cn/1669/list.htm","财大综合新闻",headers = one_header)
    
    # 数要翻页的次数
    print("查询页数中...")
    zuelCrawler_1669.countPageNum()
    print(zuelCrawler_1669.getPageNum())
    
    # 获取要爬取的url
    print("翻页中...")
    zuelCrawler_1669.getUrls(startpage = 1,endpage = zuelCrawler_1669.getPageNum(),urlsfile_path="./data/zuelurls-综合新闻.csv")

    # 华科学校要闻
    HustCrawler_zhxw = HustCrawler("http://news.hust.edu.cn/zhxw.htm","华科综合新闻",headers = one_header)
    
    # 数要翻页的次数
    print("查询页数中...")
    HustCrawler_zhxw.countPageNum()
    print(HustCrawler_zhxw.getPageNum())
    
    # 获取要爬取的url
    print("翻页中...")
    HustCrawler_zhxw.getUrls(startpage = 1,endpage = HustCrawler_zhxw.getPageNum(),urlsfile_path="./data/husturls-综合新闻.csv")
    
    # 测试parse函数
    # zuelCrawler_1669.parse(url='http://wellan.zuel.edu.cn/2022/0921/c1668a306614/page.htm')
    
    # 爬取
    # print("爬取中...")
    # zuel
    # crawlZuel(urlsfile_path="./data/zuelurls-文澜要闻.csv",save_path="./data/zuel_news/文澜要闻/",startrow=1400)
    # hust
    # crawlHust(urlsfile_path="./data/husturls-学校要闻.csv",save_path="./data/hust_news/学校要闻/",startrow=270)

