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

        def extract_with_xpath(query):
            return response.xpath(query).getall()

        # Save content
        yield {
            "job_title": extract_with_css("#detail-el h1.main-title span::text"),
            "company_title": extract_with_css("#detail-el h2.desc-for-title span::text"),
            "updated_date": response.xpath(".//p[strong/text() = 'Ngày duyệt: ']/text()").get(default=''),
            "details_job": {
                "work_location": extract_with_xpath(".//p[strong/text() = 'Địa điểm tuyển dụng: ']/span/a/text()"),
                "category": extract_with_xpath(".//div[p/strong/text() = 'Ngành nghề:']/span/a/text()"),
                "level": extract_with_xpath(".//p[strong/text() = 'Chức vụ:']/text()"),
                "salary": extract_with_xpath(".//p[strong/text() = 'Mức lương:']/span/text()"),
                "deadline": extract_with_xpath(".//p[strong/text() = 'Hạn nộp hồ sơ:']/span/text()"),
                "experience": extract_with_xpath(".//p[strong/text() = 'Kinh nghiệm:']/text()")
            },
            "job_description": response.xpath(".//h3[text() = 'Mô tả công việc ']/following-sibling::div[1]").getall(),
            "job_requirement": response.xpath(".//h3[text() = 'Yêu cầu công việc']/following-sibling::div[1]").getall(),
            "other_information": response.xpath(".//h3[text() = 'Yêu cầu hồ sơ']/following-sibling::div[1]").getall(),

            "entitlements": response.xpath(".//h3[text() = 'Quyền lợi được hưởng']/following-sibling::div[1]").getall(),
            #"tags": response.xpath(".//div[span/text() = 'Job tags / Kỹ năng:']/a").getall(),
        }

