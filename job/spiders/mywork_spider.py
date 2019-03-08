# -*- coding: utf-8 -*-
import scrapy
from job.spiders.template_spider import TemplateSpider

class MyworkSpider(TemplateSpider):
    name = 'mywork'
    allowed_domains = ['mywork.com.vn']
    start_urls = [
        'https://mywork.com.vn/tuyen-dung'
    ]

    def parse(self, response):
        # follow links to detail job pages
        item_links = response.css("#idJobNew .box-body .item-list .item p.j_title a.el-tooltip::attr(href)").extract()
        for a in item_links:
            yield response.follow(url=a, callback=self.parse_job_detail)

        # follow pagination links
        next_links = response.xpath(".//a[span/text()='Trang sau']/@href").getall()
        for href in next_links:
            yield response.follow(url=href, callback=self.parse)

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

        yield self.get_item(source_url=response.url,
                            job_title=extract_with_css("#detail-el h1.main-title span::text"),
                            company_title=extract_with_css("#detail-el h2.desc-for-title span::text"),
                            updated_date=response.xpath(".//p[strong/text() = 'Ngày duyệt: ']/text()").get(default=''),
                            work_location=extract_formatted_with_xpath(".//strong[contains(text(), 'Địa điểm tuyển dụng:')]/following-sibling::span[1]/a/text()"),
                            category=extract_formatted_with_xpath(".//div[p/strong/text() = 'Ngành nghề:']/span/a/text()"),
                            salary=extract_formatted_with_xpath(".//p[strong/text() = 'Mức lương:']/span/text()"),
                            level=extract_one_with_xpath(".//p[strong/text() = 'Chức vụ:']/text()"),
                            deadline=extract_one_with_xpath(".//p[strong/text() = 'Hạn nộp hồ sơ:']/span/text()"),
                            experience=extract_one_with_xpath(".//p[strong/text() = 'Kinh nghiệm:']/text()"),
                            job_description=extract_formatted_with_xpath(".//h3[text() = 'Mô tả công việc ']/following-sibling::div[1]"),
                            job_requirement=extract_formatted_with_xpath(".//h3[text() = 'Yêu cầu công việc']/following-sibling::div[1]"),
                            other_information=extract_formatted_with_xpath(".//h3[text() = 'Yêu cầu hồ sơ']/following-sibling::div[1]"),
                            tags="")



