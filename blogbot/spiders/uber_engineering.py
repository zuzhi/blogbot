# -*- coding: utf-8 -*-
import scrapy


class UberEngineeringSpider(scrapy.Spider):
    name = 'uber_engineering'
    allowed_domains = ['eng.uber.com']
    start_urls = ['https://eng.uber.com']

    def parse(self, response):
        for item in response.css('div.td-main-content div.item-details'):
            link = item.css('h3.entry-title>a::attr(href)').extract_first()

            post = {
                'title': item.css('h3.entry-title>a::text').extract_first(),
                'link': link,
                'date': item.css('time.entry-date::text').extract_first(),
                'datetime': item.css('time::attr(datetime)').extract_first(),
                'excerpt': item.css('div.td-excerpt::text').extract_first().strip()
            }

            request = scrapy.Request(url=link, callback=self.parse_post)
            request.meta['post'] = post
            yield request

        next_page_url_icon = response.css('div.page-nav>a:last-of-type>i.td-icon-menu-right')
        if next_page_url_icon is not None:
            next_page_url = response.css('div.page-nav>a:last-of-type::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_post(self, response):
        post = response.meta['post']
        categories = []
        for item in response.css('li.entry-category'):
            categories.append(item.css('a::text').extract_first())
        post['categories'] = categories
        yield post