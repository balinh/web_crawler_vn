# -*- coding: utf-8 -*-
import scrapy
from tuoitre_crawler.items import TuoitreCrawlerItem

class TuoitreCrawlerBotSpider(scrapy.Spider):
    name = 'tuoitre_crawler'
    allowed_domains = ['http://tuoitre.vn']

    start_urls = []
    begin_url = 'http://tuoitre.vn/undefined/xem-theo-ngay/'
    categoryDict = {'thời sự': 'news', 'thế giới': 'world', 'kinh doanh': 'business', 'giải trí': 'entertainment',
                    'thể thao': 'sport', 'pháp luật': 'legal', 'giáo dục': 'education', 'gia đình': 'family',
                    'du lịch': 'travel', 'khoa học': 'science', 'số hóa': 'technology', 'xe': 'vehicle',
                    'cộng đồng': 'community', 'doanh nghiệp': 'company', 'quân sự': 'military',
                    'quốc tế': 'international',
                    'bất động sản': 'real estate', 'ebank': 'bank', 'ngân hàng': 'bank', 'thương mại': 'commerce',
                    'thương mại điện tử': 'commerce', 'chứng khoán': 'stock', 'phim': 'film', 'nhạc': 'music',
                    'thời trang': 'fashion', 'truyền hình': 'tv', 'sách': 'book', 'bóng đá': 'football',
                    'tổ ấm': 'home', 'chăm con': 'child care', 'nhà đẹp': 'house', 'tiêu dùng': 'consumer',
                    'nội trợ': 'housework', 'việt nam': 'vietnam', 'sản phẩm': 'product', 'điện tử gia dụng': 'electronic',
                    'xã hội': 'society', 'yêu': 'love', 'tư vấn': 'advisory', 'tài chính': 'finance',
                    'đầu tư': 'invest', 'nhà đất': 'real estate', 'điện thoại': 'mobile', 'thiết bị số': 'digital device',
                    'đánh giá': 'review', 'bảo mật': 'security', 'thủ thuật': 'tips', 'văn hóa': 'culture',
                    'trải nghiệm - khám phá': 'discover', 'ẩm thực': 'food', 'nhịp sống trẻ': 'youth', 'xu hướng':
                    'trend', 'khám phá': 'discover', 'việc làm': 'jobs', 'đời sống': 'life', 'văn học': 'literary',
                    'điện ảnh': 'film', 'hậu trường': 'backstage', 'quần vợt': 'tennis', 'dinh dưỡng': 'nutrition',
                    'chính trị': 'politic', 'giao thông': 'traffic', 'địa ốc': 'real estate',
                    'môi trường': 'environment', 'âm nhạc': 'music', 'làm đẹp': 'make up',
                    'giới tính': 'sex', 'điện tử': 'electronic', 'máy tính': 'computer', 'viễn thông': 'telecommunication',
                    'di động': 'mobile', 'mạng': 'network', 'phần mềm': 'software',
                    'pháp lý': 'legal', 'thị trường': 'market',
                    }

    start_year = 2005
    end_year = 2017
    start_month = 1
    end_month = 12
    start_day = 1
    end_day = 30

    for year in range(start_year, end_year + 1):
        for month in range(start_month, end_month + 1):
            for day in range(start_day, end_day + 1):
                start_urls.append(begin_url + str(day) + '-' + str(month) + '-' + str(year) + ".htm")

    def parse(self, response):
        for href in response.xpath("//h3/a[contains(@class, 'ff-bold')]//@href"):
            url = 'http://tuoitre.vn' + href.extract()
            yield scrapy.Request(url, callback=self.parse_news_contents, dont_filter=True)

    def parse_title(self, response):
        title = ''
        titles = response.xpath("//h1[contains(@class, 'title') or contains(@id, 'title')]/descendant::text()").extract()
        if len(titles) > 0:
            for str in titles:
                if len(str.strip()) > 0:
                    title = str.strip().lower()
                    break
        return title
        
    def parse_summary(self, response):
        summary = ''
        summaries = response.xpath("//h2[contains(@class, 'txt-head')]/descendant::text()").extract()

        if len(summaries) > 0:
            for str in summaries:
                if len(str.strip()) > 0:
                    summary = str.strip().lower()
                    break

        return summary
        
    def parse_tags(self, response):
        tagstr = ''
        tags = response.xpath("//ul[contains(@class, 'block-key')]//a[@itemprop = 'keywords']/@title").extract()
        if len(tags) != 0:
            tagstr = ",".join([tag.strip().lower() for tag in tags])
        else:
            tagstr = ""
        return tagstr

    def parse_categories(self, response):
        catStr = ''
        categories = response.xpath("//div[contains(@class, 'category')]//a/text()").extract()
        if len(categories) > 0:
            catStr = self.categoryDict.get(categories[0].strip().lower(), '')
            if len(categories) > 1:
                cat = self.categoryDict.get(categories[1].strip().lower(), '')
                if cat != '':
                    if catStr != '':
                        catStr += ',' + cat
                    else:
                        catStr = cat

            section = response.xpath("//meta[contains(@property, 'section')]/@content").extract()
            if len(section) > 0:
                cat = self.categoryDict.get(section[0].strip().lower(), '')
                if cat != '' and cat != catStr:
                    catStr += ',' + cat
        return catStr

    def parse_paragraphs(self, response):
        paraStr = ''
        paragraphs = response.xpath("//p[contains(@class, 'pBody')]/descendant::text()").extract()            
        if len(paragraphs) == 0:
            paragraphs = response.xpath("//p/descendant::text()").extract()

        if len(paragraphs) != 0:
            paragraphs = [x.strip() for x in paragraphs if len(x.strip()) > 0]
            paraStr = " ".join(paragraphs).lower()            
                        
        return paraStr
    
    def parse_news_contents(self, response):
        item = TuoitreCrawlerItem()

        item['text'] = self.parse_paragraphs(response)
        if len(item['text']) != 0:
            item['title'] = self.parse_title(response)
            item['summary'] = self.parse_summary(response)
            item['text'] = item['title'] + ". " + item['text']
            item['tags'] = self.parse_tags(response)
            item['category'] = self.parse_categories(response)
            item['url'] = response.url

            yield item


