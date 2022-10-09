# SchoolNewsCrawler
《非结构化数据分析》课程作业-爬取中南财和华科的新闻，用于文本二分类任务

👐项目工具：
- selenium
- python3.8
- Firefox

这辈子不想用zuel-dorm(zuel的宿舍校园网)调试/运行任何一只爬虫……

大学最无语的课程作业，应该就是爬财大和华科新闻网……爬！

我遇到了不下两三个需要我折腾两三个小时反常的bug……

1. 按常理，request接受响应的速度快于selenium，但是在zuel-dorm下，这点不成立……用request，要开多进程，但是没折腾成功……
2. ️想不完全加载页面，想用selenium的显示等待……用了半天没用明白……最后直接更改page load strategy
3. ️明明前两天还能速爬的代码，今天换个参数再运行就巨慢，合着薛定谔的校园网？
4. ️不要在try-except语句中的except里写`return None`，不然你不知道你是怎么死的

综上，不要用校园网写爬虫作业/构建web程序;不要轻易接触爬虫;selenium真香