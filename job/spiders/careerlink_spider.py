# -*- coding: utf-8 -*-
import scrapy
from job.spiders.template_spider import TemplateSpider

class CareerlinkSpider(TemplateSpider):
    name = 'careerlink'
    allowed_domains = ['www.careerlink.vn']
    start_urls = [
        'https://www.careerlink.vn/vieclam/list?keyword_use=A'
    ]

    def parse(self, response):
        # follow links to detail job pages
        item_links = response.css("#save-job-form h2.list-group-item-heading a::attr(href)").extract()
        for a in item_links:
            print('Processing..' + response.url)
            yield response.follow(url=a, callback=self.parse_job_detail)

        # follow pagination links
        next_links = response.xpath(".//a[span/text()='Tiếp tục']/@href").getall()
        for href in next_links:
            yield response.follow(url=href, callback=self.parse)

    def parse_job_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_with_xpath(query):
            return response.xpath(query).getall()

        def extract_one_with_xpath(query):
            return response.xpath(query).get(default='').strip()

        # Save content
        yield {
            "job_title": extract_with_css(".job-header h1 span::text"),
            "company_title": extract_with_css(".critical-job-data li a > span > span::text"),
            "updated_date": response.xpath(".//dt[text()='Ngày gởi: ']/following-sibling::dd[1]/text()").get().strip(),
            "details_job": {
                "work_location": extract_one_with_xpath('.//span[contains(@itemprop, "streetAddress")]/text()') +
                        extract_one_with_xpath('.//span[contains(@itemprop, "addressLocality")]/text()') +
                        extract_one_with_xpath('.//span[contains(@itemprop, "addressRegion")]/text()') +
                        extract_one_with_xpath('.//span[contains(@itemprop, "addressCountry")]/text()') ,
                "category": extract_one_with_xpath(".//li[contains(text(), 'Ngành nghề việc làm:')]/ul/li/a/span/text()"),
                "level": " ".join( response.xpath(".//li[contains(text(), 'Cấp bậc')]/text()").get().strip().split()[2:] ),
                "salary": extract_one_with_xpath('//span[contains(@itemprop, "baseSalary")]/span/text()'),
                "deadline": extract_one_with_xpath(".//dt[text() = 'Ngày hết hạn: ']/following-sibling::dd[1]/span/text()"),
                "experience": extract_one_with_xpath(".//span[contains(@itemprop, 'experienceRequirements')]/text()")
            },
            "job_description": extract_with_xpath('.//div[contains(@itemprop, "description")]'),
            "job_requirement": extract_with_xpath('.//div[contains(@itemprop, "skills")]'),
            "other_information": response.xpath(".//h2[text() = 'Thông tin liên hệ']/following-sibling::ul[1]").getall(),

            "tags": response.xpath('//a[contains(@class, "tag")]/text()').getall(),
            #"entitlements": response.xpath(".//h3[text() = 'Quyền lợi được hưởng']/following-sibling::div[1]").getall(),
        }

