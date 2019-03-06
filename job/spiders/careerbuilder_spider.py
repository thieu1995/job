# -*- coding: utf-8 -*-
import scrapy
from job.spiders.template_spider import TemplateSpider

class CareerbuilderSpider(TemplateSpider):
    name = 'careerbuilder'
    allowed_domains = ['careerbuilder.vn']
    start_urls = [
        'https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-vi.html'
    ]

    # def parse(self, response):
    #     # Crawl brief information about job
    #     for job in response.css(".gird_standard dd.brief"):
    #         yield {
    #             "title": job.css(".jobtitle h3.job a::text").get(),
    #             "company": job.css(".jobtitle p.namecom a::text").get(),
    #             "locations": job.css(".jobtitle p.location::text").get(),
    #             "salary": job.css(".jobtitle p.salary::text").get(),
    #             "updated_date": job.css(".dateposted::text").get()
    #         }
    #     next_page_url = response.css(".paginationTwoStatus > a.right::attr(href)").get()
    #     if next_page_url is not None:
    #         yield scrapy.Request(next_page_url, callback=self.parse)


    def parse(self, response):
        # follow links to detail job pages
        item_links = response.css(".jobtitle h3.job a::attr(href)").extract()
        for a in item_links:
            yield scrapy.Request(url=a, callback=self.parse_job_detail)

        # follow pagination links
        next_links = response.css(".paginationTwoStatus > a.right::attr(href)").extract()
        for href in next_links:
            yield scrapy.Request(href, self.parse)

    def parse_job_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_with_xpath(query):
            return response.xpath(query).getall()

        # Save content
        yield {
            "job_title": extract_with_css(".top-job-info h1::text"),
            "company_title": extract_with_css(".top-job-info .tit_company::text"),
            "updated_date": extract_with_css(".datepost > span::text"),
            "details_job": {
                "work_location": extract_with_xpath(".//p[span/text() = 'Nơi làm việc: ']/b/a/text()"),
                "category": extract_with_xpath(".//p[span/text() = 'Ngành nghề: ']/b/a/text()"),
                "level": extract_with_xpath(".//p[span/text() = 'Cấp bậc: ']/label/text()"),
                "salary": extract_with_xpath(".//p[span/text() = 'Lương: ']/label/text()"),
                "deadline": extract_with_xpath(".//p[span/text() = 'Hết hạn nộp: ']/text()"),
                "experience": extract_with_xpath(".//p[span/text() = 'Kinh nghiệm: ']/text()")
            },
            "job_description": response.xpath(".//div[h4/text() = 'Mô tả Công việc']/div").getall(),
            "job_requirement": response.xpath(".//div[h4/text() = 'Yêu Cầu Công Việc']/div").getall(),
            "other_information": response.xpath(".//div[h4/text() = 'Thông tin khác']/div").getall(),
            "tags": response.xpath(".//div[span/text() = 'Job tags / Kỹ năng:']/a").getall(),
        }

