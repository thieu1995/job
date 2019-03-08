import scrapy
from job.items import JobItem
from job import crawl_limit

class TemplateSpider(scrapy.Spider):
    name = 'template'
    page_limit = 1
    crawl_count = 0
    filename = None
    testing = False
    allowed_domains = ['//no domain']
    directory = './'

    def __init__(self, name=None, **kwargs):
        super(TemplateSpider, self).__init__(name, **kwargs)
        self.page_limit = crawl_limit.limit.get(self.name, 1)

    def parse(self, response):
        raise NotImplementedError()

    def parse_content(self, response):
        raise NotImplementedError()

    def get_item(self, source_url, job_title, company_title, updated_date, work_location, category, salary, level, deadline,
                 experience,job_description, job_requirement, other_information, tags):
        self.crawl_count += 1
        return JobItem(source=self.name, source_url=source_url,job_title=job_title,
                        company_title=company_title, updated_date=updated_date,
                        work_location=work_location, category=category,
                        salary=salary, level=level, deadline=deadline, experience=experience,
                        job_description=job_description, job_requirement=job_requirement,
                        other_information=other_information, tags=tags)