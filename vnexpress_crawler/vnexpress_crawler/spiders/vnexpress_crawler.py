# -*- coding: utf-8 -*-
import scrapy
from vnexpress_crawler.items import VnexpressCrawlerItem

class VnexpressCrawler(scrapy.Spider):
    name = 'vnexpress_crawler'
    allowed_domains = ['https://vnexpress.net']
    start_urls = []
    begin_urls = ['https://vnexpress.net/tin-tuc/thoi-su/', 'https://vnexpress.net/tin-tuc/the-gioi/',
                  'https://kinhdoanh.vnexpress.net/', 'https://giaitri.vnexpress.net/',
                  'https://thethao.vnexpress.net/', 'https://vnexpress.net/tin-tuc/phap-luat/',
                  'https://vnexpress.net/tin-tuc/giao-duc/', 'https://giadinh.vnexpress.net/',
                  'https://dulich.vnexpress.net/', 'https://vnexpress.net/tin-tuc/khoa-hoc/',
                  'https://sohoa.vnexpress.net/', 'https://vnexpress.net/tin-tuc/oto-xe-may/',
                  'https://vnexpress.net/tin-tuc/cong-dong/']

    categoryDict = {'thời sự': 'news', 'thế giới': 'world', 'kinh doanh': 'business', 'giải trí': 'entertainment',
                    'thể thao': 'sport', 'pháp luật': 'legal', 'giáo dục': 'education', 'gia đình': 'family',
                    'du lịch': 'travel', 'khoa học': 'science', 'số hóa': 'technology', 'xe': 'vehicle',
                    'cộng đồng': 'community', 'doanh nghiep': 'company', 'quân sự': 'military', 'quốc tế': 'international',
                    'bất động sản': 'real estate', 'ebank': 'bank', 'ngân hàng': 'bank', 'thương mại': 'commerce',
                    'thương mại điện tử': 'commerce', 'chứng khoán': 'stock', 'phim': 'film', 'nhạc': 'music',
                    'thời trang': 'fashion', 'truyền hình': 'tivi', 'sách': 'book', 'bóng đá': 'football',
                    'tổ ấm': 'home', 'chăm con': 'child care', 'nhà đẹp': 'house', 'tiêu dùng': 'consumer', 'nội trợ': 'housework',
                    'việt nam': 'vietnam', 'sản phẩm': 'product', 'điện tử gia dụng': 'electronic'}

    pages_num = [3200, 3200, 628, 1223, 1003, 1900, 900, 605, 575, 1248, 600, 1200, 600]
    #pages_num = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    num_extracted_acticles = 0

    for id in range(0, len(begin_urls)):
        start_urls.append(begin_urls[id])
        for page in range(2, pages_num[id] + 1):
            start_urls.append(begin_urls[id] + '/page/' + str(page) + ".html")

    def parse(self, response):
        for href in response.xpath("//h3[contains(@class, 'title_news')]/a//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_news_contents, dont_filter=True)

    def parse_news_contents(self, response):
        item = VnexpressCrawlerItem()

        paragraphs = response.xpath("//p[contains(@class, 'Normal')]/descendant::text()").extract()

        if len(paragraphs) != 0:
            item['url'] = response.url
            titles = response.xpath("(//h1[contains(@class, 'title_news')]|//div[contains(@class, 'title_news')])//text()").extract()

            if len(titles) > 0:
                for title in titles:
                    if len(title.strip()) > 0:
                        item['title'] = title.strip().lower()
                        break

            summaries = response.xpath("//h2[contains(@class, 'description')]//text()").extract()

            if len(summaries) > 0:
                for summary in summaries:
                    if len(summary.strip()) > 0:
                        item['summary'] = summary.strip().lower()
                        break

            paragraphs = [x.strip() for x in paragraphs if len(x.strip()) > 0]
            item['text'] = item['title'] + ". " + " ".join(paragraphs).lower()

            #tags = response.xpath("//div[contains(@class, 'block_tag')]//h5/a/@title").extract()
            tags = response.xpath("//div[contains(@class, 'block_tag')]//a[contains(@class, 'tag')]/@title").extract()
            if len(tags) != 0:
                item['tags'] = ",".join([tag.strip().lower() for tag in tags])
            else:
                item['tags'] = ""

            categories = response.xpath("//ul[starts-with(@class,'breadcrumb')]//a//text()").extract()

            if len(categories) > 0:
                item['category'] = self.categoryDict.get(categories[0].strip().lower(), '')
                if len(categories) > 1:
                    cat = self.categoryDict.get(categories[1].strip().lower(), '')
                    if cat != '':
                        item['category'] += ',' + cat

            self.num_extracted_acticles += 1
            print("Extracted articles: %d" % self.num_extracted_acticles)

            yield item




