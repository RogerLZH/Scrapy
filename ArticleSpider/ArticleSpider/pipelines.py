# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
import MySQLdb.cursors

from twisted.enterprise import adbapi

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

#将爬取的数据存到MySql数据库中
#这是一种同步操作，因为数据库的插入速度更不上爬虫的爬去速度，爬到后面会出现堵塞
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'lzh', 'lzh0219.lg', 'articlespider', charset = "utf8", use_unicode = True)      #连接数据库
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = "insert into articleinfo (title, date, url, url_object_id, front_image_url, front_image_path, praise_num, fav_num, comment_num, tag) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(insert_sql, (item["title"], item["date"], item["url"], item["url_object_id"], item["front_image_url"], item["front_image_path"], item["praise_num"], item["fav_num"], item["comment_num"], item["tags"]))
        self.conn.commit()       #执行SQL语句


class MySqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        #将参数变成dict,这里的参数名要和MySQLdb里的Connection中的参数名一至
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用Twisted将MySQL插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)  # 处理异常

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = "insert into articleinfo (title, date, url, url_object_id, front_image_url, front_image_path, praise_num, fav_num, comment_num, tag) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_sql, (item["title"], item["date"], item["url"], item["url_object_id"], item["front_image_url"], item["front_image_path"], item["praise_num"], item["fav_num"], item["comment_num"], item["tags"]))


class ArticleImagePipeline(ImagesPipeline):         #下载图片，并将存储地址并存到item中
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        return item