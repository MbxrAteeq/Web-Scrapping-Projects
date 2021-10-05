import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        #title = response.xpath("//h1/text()").get()
        #countries = response.xpath("//td/a/text()").getall()
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            #yield scrapy.Request(url= "https://www.worldometers.info"+link)

            #absolute_link = response.urljoin(link)
            #yield scrapy.Request(url= absolute_link)

            yield response.follow(url=link,callback=self.parse_country,meta={'country_name':name})

            #yield{
            #    "country_name":name,
            #    "country_link":link
            #}


    def parse_country(self, response):
        #logging.info(response.url)
        name = response.request.meta['country_name']
        rows = response.xpath("//table[@class='table table-striped table-bordered table-hover table-condensed table-list'][1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield{
                "Country_name":name,
                "Year":year,
                "Population":population
            }
#to save data in csv,json and xml use that cmd only change extention 
#scrapy crawl countries -o population_dataset.csv