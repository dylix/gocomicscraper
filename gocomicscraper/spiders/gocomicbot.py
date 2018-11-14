# -*- coding: utf-8 -*-
import scrapy
import functools as ft
import logging
import datetime

mycounter = 0


class GocomicbotSpider(scrapy.Spider):
    name = 'gocomicbot'
    allowed_domains = ['explosm.net', 'xkcd.org', 'gocomics.com']
    start_urls = ['http://explosm.net/comics/latest', 'https://xkcd.org',  'https://www.gocomics.com/comics/a-to-z']
    custom_settings = {
        'DOWNLOAD_DELAY' : '1.0',
        #'CLOSESPIDER_PAGECOUNT' : '5',
        'ROBOTSTXT_OBEY' : 'false',
        'CONCURRENT_REQUESTS' : '1',
    }
    
    def countme(blah):
        global mycounter
        mycounter += 1
        return mycounter
        
    def parse(self, response):
        explosm_img = response.xpath("//img[@id='main-comic']//@src").extract()
        xkcd_img = response.xpath("//div[@id='comic']//img/@src").extract()
        mydate = datetime.datetime.now()
                
        if len(explosm_img) == 1:
            yield {
                'title' : 'Cyanide and Happiness',
                'id' : self.countme(),
                'author' : 'Unknown',
                'url' : 'http://explosm.net/comics/latest',
                'image' : explosm_img,
                'date' : mydate.strftime("%B %d, %Y")
            }

        if len(xkcd_img) == 1:
            yield {
                'title' : 'XKCD',
                'id' : self.countme(),
                'author' : 'Randall Munroe',
                'url' : 'https://xkcd.com',
                'image' : xkcd_img,
                'alttext' : response.xpath("//div[@id='comic']//img/@title").extract(),
                'date' : mydate.strftime("%B %d, %Y")
            }        
        sortedlist = sorted(response.css(".gc-blended-link.gc-blended-link--primary.col-12.col-sm-6.col-lg-4::attr(href)").extract(),key=None,reverse=True)
        
        for url in sortedlist:
            yield response.follow(url, self.parse_comic)
            
    def parse_comic(self, response):
        counter_amount = self.countme()
        yield {
            'title' : response.xpath("//div/@data-feature-name").extract(),
            #'id' : response.xpath("//div/@data-feature-id").extract(),
            'id' : counter_amount,
            'author' : response.xpath("//div/@data-creator").extract(),
            'url' : response.xpath("//div/@data-url")[0].extract(),
            'image' : response.xpath("//div/@data-image").extract(),
            'width' : response.xpath("//meta[@property='og:image:width']/@content").extract(),
            'height' : response.xpath("//meta[@property='og:image:height']/@content").extract(),
            'date' : response.xpath("//div/@data-formatted-date").extract(),
        }