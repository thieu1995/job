# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import json
import datetime

class JobPipeline(object):
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'thieunv', 'NguyeN.thieu.2102','jobweb', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            insert_data = ("INSERT INTO job ""(source, source_url, import_datetime, job_title, company_title, updated_date, work_location, category, salary, level, deadline, experience, job_description, job_requirement, other_information, tags)"" "
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)")
            self.cursor.execute(insert_data, (item['source'], item['source_url'], datetime.datetime.today(),
                                              item['job_title'], item['company_title'], item['updated_date'],
                                              ';'.join(item['work_location']), ';'.join(item['category']),
                                              ' '.join(item['salary']), item['level'],  item['deadline'],
                                              item['experience'], ' '.join(item['job_description']),
                                              ' '.join(item['job_requirement']),
                                              ' '.join(item['other_information']), ';'.join(item['tags'])))
            self.conn.commit()
            print("import success")
        except MySQLdb.Error as e:
            print("Error %s:" % (e.arg[0], e.arg[1]))
        return item
