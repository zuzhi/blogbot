# -*- coding: utf-8 -*-
import scrapy


class BaeldungSpider(scrapy.Spider):
    name = 'baeldung'
    allowed_domains = ['courses.baeldung.com']
    start_urls = ['https://courses.baeldung.com/p/rest-with-spring-the-master-class']

    # start_urls = ['https://courses.baeldung.com/p/rest-with-spring-starter',
    # 'https://courses.baeldung.com/p/rest-with-spring-the-intermediate-class',
    # 'https://courses.baeldung.com/p/rest-with-spring-the-master-class']

    def parse(self, response):
        modules = response.css('.course-section')
        course = {}
        lessons = []

        for module in modules:
            module_title = ''.join(module.xpath('div[@class="section-title"]/text()').extract()).strip()
            lessons.append(module_title)
            items = module.css('.section-item')
            for i, item in enumerate(items):
                lesson_name = ' '.join((''.join(item.xpath('a[@class="item"]/text()').extract()).strip()).split())
                lessons.append(lesson_name)

        course['lessons'] = lessons
        yield course

    # def parse(self, response):
    #     modules = response.css('.course-section')
    #     for module in modules:
    #         module_title = ''.join(module.xpath('div[@class="section-title"]/text()').extract()).strip()
    #         lessons = []

    #         items = module.css('.section-item')
    #         for item in items:
    #             lesson = {}
    #             lesson['lesson_name'] = ' '.join((''.join(item.xpath('a[@class="item"]/text()').extract()).strip()).split())
    #             lessons.append(lesson)

    #         yield {
    #             'module_title': module_title,
    #             'lessons': lessons
    #         }