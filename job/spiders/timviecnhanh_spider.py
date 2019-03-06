# -*- coding: utf-8 -*-
import scrapy
from job.spiders.template_spider import TemplateSpider

class TimviecnhanhSpider(TemplateSpider):
    name = 'timviecnhanh'
    allowed_domains = ['timviecnhanh.com']
    start_urls = [
        "https://www.timviecnhanh.com/vieclam/timkiem?tu_khoa=&nganh_nghe%5B%5D=&tinh_thanh%5B%5D=",
    ]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('td.block-item a.item::attr(href)'):
            yield response.follow(href, callback=self.parse_detail)

        # follow pagination links
        #         for index_page in range(2, 5):
        #             next_page_ulr = "https://www.timviecnhanh.com/vieclam24h?page=" + str(index_page)
        #             yield response.follow(next_page_ulr, callback=self.parse)

        next_link = response.css(".page-navi a.next::attr(href)").get()
        if next_link is not None:
            print("==================Next: ", next_link)
            yield scrapy.Request(url=next_link, callback=self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'title': extract_with_css('header.block-title span.text::text'),
            # 'company_name': extract_with_css('div.col-xs-6 a::text'),
            # 'company_address': extract_with_css('div.col-xs-6 span::text'),
            # 'muc_luong': response.css('div.row div.col-xs-4 li.m-b-5')[0].re_first(r'\w+-\w+ triệu'),
            # 'kinh_nghiem': ' '.join(response.css('div.row div.col-xs-4 li.m-b-5')[1].get().strip().split()[5:-1]),
            # 'trinh_do': ' '.join(response.css('div.row div.col-xs-4 li.m-b-5')[2].get().strip().split()[5:-1]),
            # 'tinh_thanh_pho': ' '.join(response.css('div.row div.col-xs-4 li.m-b-5')[3].get().strip().split()[5:-1]),
            # 'nganh_nghe': ' '.join(response.css('div.row div.col-xs-4 li.m-b-5')[4].get().strip().split()[5:-1]),
            # 'so_luong_tuyen_dung': ' '.join(
            #     response.css('div.row div.col-xs-4 li.m-b-5')[5].get().strip().split()[7:-1]),
            # 'gioi_tinh': ' '.join(response.css('div.row div.col-xs-4 li.m-b-5')[6].get().strip().split()[5:-1]),
            # 'tinh_chat_cong_viec': ' '.join(
            #     response.css('div.row div.col-xs-4 li.m-b-5')[7].get().strip().split()[7:-1]),
            # 'hinh_thuc_lam_viec': ' '.join(
            #     response.css('div.row div.col-xs-4 li.m-b-5')[8].get().strip().split()[7:-1]),
            # 'mo_ta': ' '.join(response.css('table tbody tr td')[1].get().strip().split()[1:-1]),
            # 'yeu_cau': ' '.join(response.css('table tbody tr td')[3].get().strip().split()[1:-1]),
            # 'quyen_loi': ' '.join(response.css('table tbody tr td')[5].get().strip().split()[1:-1]),
            # 'han_nop': ' '.join(response.css('table tbody tr td')[7].get().strip().split()[1:-1]),
            # 'nguoi_lien_he': ' '.join(
            #     response.css('div.block-content table.width-100 td')[1].get().strip().split()[1:-1]),
            # 'dia_chi_nguoi_lien_he': ' '.join(
            #     response.css('div.block-content table.width-100 td')[3].get().strip().split()[1:-1]),
        }