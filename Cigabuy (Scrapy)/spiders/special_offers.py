# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com']
    start_urls = ['https://www.cigabuy.com/specials.html']

    def parse(self, response):
        offers = response.xpath("//ul[@class='productlisting-ul']/div[@class='p_box_wrapper']/div")
        for offer in offers:
            title = offer.xpath(".//a[@class='p_box_title']/text()").get()
            url = offer.xpath(".//a[@class='p_box_title']/@href").get()
            discount = offer.xpath(".//div[@class='p_box_price cf']/span[@class='normalprice fl']/text()").get()
            price = offer.xpath(".//div[@class='p_box_price cf']/span[@class='productSpecialPrice fl']/text()").get()

            yield{
                'title':title,
                'url':url,
                'discount':discount,
                'price':price
            }

        next_page = response.xpath("//a[@class='nextPage']/@href").get()
        
        if next_page:
            yield scrapy.Request(url=next_page,callback=self.parse)