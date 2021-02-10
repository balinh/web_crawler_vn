# -*- coding: utf-8 -*-
import scrapy
from genk_crawler.items import GenkCrawlerItem
from scrapy.exceptions import CloseSpider


class GenkCrawlerSpider(scrapy.Spider):
    name = 'genk_crawler'
    allowed_domains = ['http://genk.vn']
    base_url = 'http://genk.vn/ajax-home/page-{0}/20171107133745743.chn'
    pageid = 1
    start_urls = [base_url.format(pageid)]
    page_deep = 8000
    
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

    def parse(self, response):
        links = response.xpath("(//h2|//h3|//h4)[contains(@class, 'title')]//@href")
        if (self.pageid < self.page_deep) or (len(links) > 0):
            for href in links:
                if href.extract().find('javascript') == -1:
                    url = 'http://genk.vn' + href.extract()
                    yield scrapy.Request(url, callback=self.parse_news_contents, dont_filter=True)
        else:
            raise CloseSpider('Crawled {0} pages \n <---------- End page ---------->'.format(self.pageid))
        
        self.pageid += 1
        yield scrapy.Request(self.base_url.format(self.pageid), callback=self.parse, dont_filter=True)
            
    def parse_title(self, response):
        title = ''
        titles = response.xpath("//h1[contains(@class, 'title')]//text()").extract()
        if len(titles) > 0:
            for str in titles:
                if len(str.strip()) > 0:
                    title = str.strip().lower()
                    break
        return title
        
    def parse_summary(self, response):
        summary = ''
        summaries = response.xpath("//h2//text()").extract()

        if len(summaries) > 0:
            for str in summaries:
                if len(str.strip()) > 0:
                    summary = str.strip().lower()
                    break

        return summary
        
    def parse_tags(self, response):
        tagstr = ''
        tags = response.xpath("//div[contains(@class, 'tags')]/ul//@title").extract()
        if len(tags) != 0:
            tagstr = ",".join([tag.strip().lower() for tag in tags])
        else:
            tagstr = ""

        return tagstr

    def parse_categories(self, response):
        catStr = ''
        categories = response.xpath("//div[contains(@class, 'breakcrum')]//span[contains(@itemprop, 'name')]/text()").extract()
        if len(categories) > 0:
            catStr = self.categoryDict.get(categories[0].strip().lower(), '')
            if len(categories) > 1:
                cat = self.categoryDict.get(categories[1].strip().lower(), '')
                if cat != '':
                    catStr = cat 
                        
        return catStr
    
    def parse_paragraphs(self, response):
        paraStr = ''
        paragraphs = response.xpath("(//div[contains(@id, 'ContentDetail')]/p | //div[contains(@id, 'ContentDetail')]/div)//text()").extract()
        if len(paragraphs) != 0:
            paragraphs = [x.strip() for x in paragraphs if len(x.strip()) > 0]
            paraStr = " ".join(paragraphs).lower()
                        
        return paraStr

    def parse_news_contents(self, response):
        item = GenkCrawlerItem()

        item['text'] = self.parse_paragraphs(response)
        if len(item['text']) != 0:
            item['title'] = self.parse_title(response)
            item['summary'] = self.parse_summary(response)
            item['text'] = item['title'] + ". " + item['text']
            item['tags'] = self.parse_tags(response)
            item['category'] = self.parse_categories(response)
            item['url'] = response.url

            yield item

