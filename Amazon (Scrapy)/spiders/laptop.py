# -*- coding: utf-8 -*-
import scrapy


class LaptopSpider(scrapy.Spider):
    name = 'laptop'
    allowed_domains = ['www.amazon.com/s?i=specialty-aps']
    start_urls = ['https://www.amazon.com/s?i=specialty-aps/']

    def parse(self, response):
        Details = response.xpath("//div[@class='s-expand-height s-include-content-margin s-border-bottom s-latency-cf-section']/div[@class='a-section a-spacing-medium']")
        for detail in Details:
            title = detail.xpath(".//div[@class='a-section a-spacing-none a-spacing-top-small']/h2/a/span/text()").get()

            yield{
                'title':title
            }
