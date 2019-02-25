# -*- coding: utf-8 -*-
import scrapy
from urllib.request import quote
from selenium import webdriver
from jingdong.items import JingdongItem


class ComputerSpider(scrapy.Spider):
    name = 'computer'
    allowed_domains = ['www.jd.com']
    base_urls = ['https://search.jd.com/Search?keyword=']

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                urls = self.base_urls[0] + quote(keyword)
                yield scrapy.Request(url=urls, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        print("数据解析")
        count = 0
        computers = response.selector.xpath(".//div[@id='J_goodsList']/ul[@class='gl-warp clearfix']/"
                                            "li[@class='gl-item']/div[@class='gl-i-wrap']")
        for computer in computers:
            item = JingdongItem()
            item["name"] = computer.xpath(".//div[@class='p-name']/a/em/text()").extract_first().replace('\n', '')\
                .replace('\t', '')
            item['url'] = "https:" + computer.xpath(".//div[@class='p-name']/a/@href").extract_first()
            item['price'] = computer.xpath(".//div[@class='p-price']/strong/i/text()").extract_first()
            # item['image'] = "https:" + computer.xpath(".//div[@class='p-img']/a/img/@src").extract_first()
            item['comments'] = computer.xpath(".//div[@class='p-commit']/strong/a/text()").extract_first()
            count += 1
            print(count)
            yield item

