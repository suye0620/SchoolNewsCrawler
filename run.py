from utils.crawler import zuelCrawler

if __name__ == "__main__":
    # 伪装的请求头
    one_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }

    # 文澜要闻
    zuelCrawler_1668 = zuelCrawler("http://wellan.zuel.edu.cn/1668/list.htm","文澜要闻",headers = one_header)
    zuelCrawler_1668.countPageNum()