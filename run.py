from utils.crawler import ZuelCrawler

if __name__ == "__main__":
    # 伪装的请求头
    one_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    }

    # 文澜要闻
    zuelCrawler_1668 = ZuelCrawler("http://wellan.zuel.edu.cn/1668/list.htm","文澜要闻",headers = one_header)
    
    # 数要翻页的次数
    # print("查询页数中...")
    # zuelCrawler_1668.countPageNum()
    # print(zuelCrawler_1668.getPageNum())
    
    # 获取要爬取的url
    # print("翻页中...")
    # zuelCrawler_1668.getUrls(startpage = 1,endpage = zuelCrawler_1668.getPageNum(),urlsfile_path="./data/zuelurls-文澜要闻.csv")
    
    # 测试parse函数
    # zuelCrawler_1668.parse(url='http://wellan.zuel.edu.cn/2022/0921/c1668a306614/page.htm')
    
    # 爬取
    print("爬取中...")
    # zuelCrawler_1668.crawl(urlsfile_path="./data/zuelurls-文澜要闻.csv",save_path="./data/zuel_news/文澜要闻/")
    zuelCrawler_1668.crawl(urlsfile_path="./data/urls.csv",save_path="./data/zuel_news/")