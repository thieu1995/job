# -*- coding: utf-8 -*-
import scrapy
from job.spiders.template_spider import TemplateSpider

class Timviec365Spider(TemplateSpider):
    name = 'timviec365'
    allowed_domains = ['timviec365.vn']
    start_urls = ['https://timviec365.vn/tin-tuyen-dung-viec-lam.html']

    def parse(self, response):
        # follow links to detail job pages
        item_links = response.css(".item_cate a.title_cate::attr(href)").getall()
        for a in item_links:
            yield response.follow(url=a, callback=self.parse_job_detail)

        # follow pagination links
        next_link = response.css(".pagination_wrap a.next::attr(href)").get()
        if next_link is not None:
            print("==========================Next Link: ", next_link)
            yield response.follow(url=next_link, callback=self.parse)

    def parse_job_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_with_xpath(query):
            return response.xpath(query).getall()

        # Save content
        yield {
            "job_title": extract_with_css(".box_tit_detail .right_tit h1::text"),
            "company_title": extract_with_css(".box_tit_detail .right_tit h2 a::text"),
            "updated_date": response.css(".xacthuc_tit p::text").getall()[1].strip().split()[3],
            "details_job": {
                "work_location": response.css(".dd_tuyen a::text").getall(),
                "category": extract_with_xpath(".//div[b/text() = 'Ngành nghề:']/span/a/text()"),
                "level": extract_with_xpath(".//div[b/text() = 'Chức vụ:']/span/text()"),
                "salary": extract_with_xpath(".//p[text() = 'Mức lương: ']/span/text()"),
                "deadline": extract_with_xpath(".//p[text() = 'Hạn nộp hồ sơ: ']/span/text()"),
                "experience": extract_with_xpath(".//div[b/text() = 'Kinh nghiệm:']/span/text()")
            },
            "job_description": response.xpath(".//div[contains(@class, 'box_mota')]").getall(),
            "job_requirement": response.xpath(".//div[contains(@class, 'box_yeucau')]").getall(),
            #"other_information": response.xpath(".//h3[text() = 'Yêu cầu hồ sơ']/following-sibling::div[1]").getall(),

            "entitlements": response.xpath(".//div[contains(@class, 'box_quyenloi')]").getall(),
            #"tags": response.xpath(".//div[span/text() = 'Job tags / Kỹ năng:']/a").getall(),
        }

