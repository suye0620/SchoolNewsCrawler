from utils.crawler import zuelCrawler

if __name__ == "__main__":
    # 伪装的请求头
    one_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    }

    # 文澜要闻
    zuelCrawler_1668 = zuelCrawler("http://wellan.zuel.edu.cn/1668/list.htm","文澜要闻",headers = one_header)
    # zuelCrawler_1668.countPageNum()
    zuelCrawler_1668.getUrls(1,2)