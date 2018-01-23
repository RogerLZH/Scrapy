# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
import datetime
import re


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + "-jobbole"


def data_convert(value):
    try:
        date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        date = datetime.datetime.now().date()
    return date


def rm_commet_tags(value):
    # 去掉tags中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


def get_num(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def return_value(value):
    return value


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(lambda x: x + "-Roger", add_jobbole)
    )
    date = scrapy.Field(
        input_processor=MapCompose(data_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        # 覆盖掉default_output_processor，否则修改了front_image_url值后下载图片的pipeline会抛异常
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_num = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    fav_num = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(rm_commet_tags),
        output_processor=Join(",")
    )
