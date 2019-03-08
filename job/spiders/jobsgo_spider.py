# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime, timedelta
from job.spiders.template_spider import TemplateSpider

class VieclamtuoitreSpider(TemplateSpider):
    name = 'jobsgo'
    allowed_domains = ['jobsgo.vn']
    start_urls = ['https://jobsgo.vn/viec-lam.html']

    def parse(self, response):
        # follow links to detail job pages
        item_links = response.css(".ad-info a.title::attr(href)").extract()
        for a in item_links:
            print('Processing..' + response.url)
            yield response.follow(url=a, callback=self.parse_job_detail)

        # follow pagination links
        next_links = response.css("li.next a::attr(href)").get()
        if next_links is not None:
            yield response.follow(url=next_links, callback=self.parse)

    def parse_job_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_one_with_xpath(query):
            return response.xpath(query).get(default='').strip()

        def extract_formatted_with_xpath(query):
            list_items = response.xpath(query).getall()
            for i in range(len(list_items)):
                list_items[i] = list_items[i].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            return list_items

        yield self.get_item(source_url=str(response.url),
                            job_title=extract_with_css(".media-body-2 h1.media-heading::text"),
                            company_title=extract_with_css(".job-detail-col-2 h2.media-heading::text"),
                            updated_date=datetime.now() - timedelta(days= int(extract_with_css(".deadline::text")) ),
                            work_location=extract_with_css(".giaphv > p > a::text"),
                            category=extract_formatted_with_xpath(".//h5[contains(text(), 'Ngành nghề')]/following-sibling::div[1]/a/text()"),
                            salary=extract_with_css("span.saraly::text"),
                            level="",
                            deadline=datetime.now() + timedelta(days= int(extract_with_css(".deadline::text")) ),
                            experience=extract_one_with_xpath(".//h5[contains(text(), 'Yêu cầu kinh nghiệm')]/following-sibling::p[1]/text()"),
                            job_description=extract_formatted_with_xpath('.//h5[contains(text(), "Mô tả công việc")]/following-sibling::div[1]'),
                            job_requirement=extract_formatted_with_xpath('.//h5[contains(text(), "Yêu cầu công việc")]/following-sibling::div[1]'),
                            other_information=extract_formatted_with_xpath(".//h5[text() = 'Quyền lợi được hưởng']/following-sibling::div[1]"),
                            tags="")

