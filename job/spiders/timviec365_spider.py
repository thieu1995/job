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
            yield response.follow(url=next_link, callback=self.parse)

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

        def extract_formatted_with_css(query):
            list_items = response.css(query).getall()
            for i in range(len(list_items)):
                list_items[i] = list_items[i].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            return list_items

        yield self.get_item(source_url=str(response.url),
                            job_title=extract_with_css(".box_tit_detail .right_tit h1::text"),
                            company_title=extract_with_css(".box_tit_detail .right_tit h2 a::text"),
                            updated_date=response.css(".xacthuc_tit p::text").getall()[1].strip().split()[3],
                            work_location=extract_formatted_with_css(".dd_tuyen a::text"),
                            category=extract_formatted_with_xpath(".//div[b/text() = 'Ngành nghề:']/span/a/text()"),
                            salary=extract_formatted_with_xpath(".//p[text() = 'Mức lương: ']/span/text()"),
                            level=extract_one_with_xpath(".//div[b/text() = 'Chức vụ:']/span/text()"),
                            deadline=extract_one_with_xpath(".//p[text() = 'Hạn nộp hồ sơ: ']/span/text()"),
                            experience=extract_one_with_xpath(".//div[b/text() = 'Kinh nghiệm:']/span/text()"),
                            job_description=extract_formatted_with_xpath(".//div[contains(@class, 'box_mota')]"),
                            job_requirement=extract_formatted_with_xpath(".//div[contains(@class, 'box_yeucau')]"),
                            other_information=extract_formatted_with_xpath(".//div[contains(@class, 'box_quyenloi')]"),
                            tags='')
