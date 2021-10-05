# -*- coding: utf-8 -*-
import scrapy


class LaptopsSpider(scrapy.Spider):
    name = 'laptops'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/laptop-deals/s?k=laptop+deals']

    def parse(self, response):
        Details = response.xpath("//div[@class='sg-col-inner']/span/div/div[@class='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16']")
        for detail in Details:
            title = detail.xpath(".//div/span/div/div//div[@class='sg-col-inner']/div[@class='a-section a-spacing-none']/h2/a/span/text()").get()
            price = detail.xpath(".//div/span/div/div//div[@class='sg-col-inner']/div[@class='sg-row']/div/div/div/div/a/span/span/text()").get()


            yield{
                'title':title,
                'price':price
            }
        next_page = response.xpath("//div[@class='a-section a-spacing-none a-padding-base']/div/ul/li[@class='a-last']/a/@href")
        if next_page:
            yield scrapy.Request(url=next_page,callback=self.parse)


#complete title xpath
#//div[@class='sg-col-inner']/span/div/div[@class='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16']/div/span/div/div//div[@class='sg-col-inner']/div[@class='a-section a-spacing-none']/h2/a/span
#price
#//div[@class='sg-col-inner']/span/div/div[@class='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16']/div/span/div/div//div[@class='sg-col-inner']/div[@class='sg-row']/div/div/div/div/a/span/span
#next page
#//div[@class='a-section a-spacing-none a-padding-base']/div/ul/li[@class='a-last']/a/@href