import requests
import re
import urlparse
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Item, Request
from scrapy.linkextractors import LinkExtractor


class PricesSpider(CrawlSpider):
    name = "prices"
    allowed_domains = ['crushprice.com']
    start_urls =['http://www.crushprice.com']
    rules = (
        Rule(LinkExtractor(allow=('.*www.crushprice.com/.*/.*')), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('.*www.crushprice.com.*')))
    )

    def parse_item(self, response):
        name = response.xpath("//div[@class='pdcthndng']/h1/text()").extract()[0]
        specs = response.xpath("//div[@id='features']//table//td/text()").extract()
        stores = response.xpath("//div[@id='stores-blk']//div[@class='shpdvone']//img/@alt").extract()

        product = {}
        product['name'] = name
        product['url'] = response.url
        product['specs'] = {}
        for i in range(0, len(specs), 2):
            product['specs'][specs[i]] = specs[i+1]
        product['stores'] = {}
        for i in range(len(stores)):
            product['stores'][stores[i]] = {}
            try:
                product['stores'][stores[i]]['price'] = response.xpath("//div[@id='stores-blk']/div[@class='ng-scope'][{}]//div[@class='shpdvfour']/div[@class='shpdvspc']/div/span[2]/text()".format(i+1)).extract()[0]
            except:
                product['stores'][stores[i]]['price'] = None
            try:
                product['stores'][stores[i]]['cod'] = response.xpath("//div[@id='stores-blk']/div[@class='ng-scope'][{}]//span[@ng-bind='affliate.cod']/text()".format(i+1)).extract()[0]
            except:
                product['stores'][stores[i]]['cod'] = None
            try:
                product['stores'][stores[i]]['delivery'] = response.xpath("//div[@id='stores-blk']/div[@class='ng-scope'][{}]//span[@ng-bind='affliate.delivery']/text()".format(i+1)).extract()[0]
            except:
                product['stores'][stores[i]]['delivery'] = None
            try:
                product['stores'][stores[i]]['shipping'] = response.xpath("//div[@id='stores-blk']/div[@class='ng-scope'][{}]//span[@ng-bind='affliate.shipping']/text()".format(i+1)).extract()[0]
            except:
                product['stores'][stores[i]]['shipping'] = None
            try:
                product['stores'][stores[i]]['emi'] = response.xpath("//div[@id='stores-blk']/div[@class='ng-scope'][{}]//span[@ng-bind='affliate.emi']/text()".format(i+1)).extract()[0]
            except:
                product['stores'][stores[i]]['emi'] = None
            try:
                url = response.xpath("//div[@id='stores-blk']/div[@class='ng-scope'][{}]//div[@class='shpdvfive']//a/@href".format(i+1)).extract()[0]
                query = urlparse.parse_qs(urlparse.urlsplit(url).query)
                product['stores'][stores[i]]['url'] = query['product_url'][0]
            except:
                product['stores'][stores[i]]['url'] = None

        return product
