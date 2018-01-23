# -*- coding: utf-8 -*-
# 爬去伯乐在线中的文章信息
# title文章发布的时间
# date文章发布的时间
# prasise_num点赞数
#fav_num收藏数
# comment_num评论数
#tag文章标签

import scrapy
import re
from scrapy.http import Request
from urllib import parse
import datetime


from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    def parse(self, response):
        """
         1.获取文章列表页中的文章url并交给scrapy下载并进行解析
         2.获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        """
        # 解析列表页中的所有文章url并交给scrapy下载并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url = parse.urljoin(response.url, post_url), meta = {"front_image_url": image_url}, callback = self.parse_detail)

        #获取下一页的url并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()   #实例化

        # # 通过xpath选取页面内容
        # front_image_url = response.meta.get("front_image_url", "")    #文章封面图
        #
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        #
        # date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·", "").strip()
        #
        # praise_num = int(response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0])
        #
        # fav_num = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # match_re_fav = re.match(".*?(\d+).*", fav_num)
        # if match_re_fav:
        #     fav_num = int(match_re_fav.group(1))
        # else:
        #     fav_num = 0
        #
        # comment_num = response.xpath("//a[@href = '#article-comment']/span/text()").extract()[0]
        # match_re_comment = re.match(".*?(\d+).*", comment_num)
        # if match_re_comment:
        #     comment_num = int(match_re_comment.group(1))
        # else:
        #     comment_num = 0
        #
        # tag_list = response.xpath("//p[@class = 'entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)
        #
        # # 通过css选择器来选取页面内容
        # # title_css = response.css(".entry-header h1::text").extract()[0]
        # # date_css = response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        #
        # #对实例化的article_item进行赋值
        # article_item["title"] = title
        # article_item["url"] = response.url
        # article_item["url_object_id"] = get_md5(response.url)
        # try:
        #     date = datetime.datetime.strptime(date, "%Y/%m/%d").date()
        # except Exception as e:
        #     date = datetime.datetime.now().date()
        # article_item["date"] = date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_num"] = praise_num
        # article_item["fav_num"] = fav_num
        # article_item["comment_num"] = comment_num
        # article_item["tags"] = tags

        #通过item loader加载item
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item = JobBoleArticleItem(), response = response)
        # item_loader.add_css()
        item_loader.add_xpath("title", '//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath("date", "//p[@class='entry-meta-hide-on-mobile']/text()")
        item_loader.add_xpath("praise_num", "//span[contains(@class, 'vote-post-up')]/h10/text()")
        item_loader.add_xpath("fav_num", "//span[contains(@class, 'bookmark-btn')]/text()")
        item_loader.add_xpath("comment_num", "//a[@href = '#article-comment']/span/text()")
        item_loader.add_xpath("tags", "//p[@class = 'entry-meta-hide-on-mobile']/a/text()")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])

        article_item = item_loader.load_item()

        yield article_item
