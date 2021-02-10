# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import datetime

class NewsItem(scrapy.Item):
    title = scrapy.Field()
    summary = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    pass


class NewsSpider(scrapy.Spider):
    name = ''
    allowed_domains = []

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
                    'pháp lý': 'legal', 'thị trường': 'market', 'kinh tế': 'economy', 'tài chính quốc tế': 'finance',
                    'công nghệ': 'technology', 'sức khỏe': 'health', 'bảo hiểm': 'insurance', 'tiền tệ': 'currency',
                    'xuất nhập khẩu': 'import and export', 'khuyến mãi': 'sale', 'quản trị': 'management', 'hạ tầng': 'infrastructure',
                    }


    def __init__(self, *a, **kwargs):
        super(NewsSpider, self).__init__(*a, **kwargs)
        self.base_urls = ()
        self.href_pattern = ""
        self.title_pattern = ""
        self.summary_pattern = ""
        self.text_pattern = ""
        self.tag_pattern = ""
        self.category_pattern = ""
        self.start_date = datetime.date.today()
        self.end_date = datetime.date.today()
        self.num_days = 0

    def init_date_browsing(self,
                 base_urls=(),
                 href_pattern="",
                 title_pattern="",
                 summary_pattern="",
                 text_pattern="",
                 tag_pattern="",
                 category_pattern="",
                 start_date=datetime.date.today(),
                 end_date=datetime.date.today(),
                 extra_cat_dict={}):

        self.base_urls = base_urls
        self.href_pattern = href_pattern
        self.title_pattern = title_pattern
        self.summary_pattern = summary_pattern
        self.text_pattern = text_pattern
        self.tag_pattern = tag_pattern
        self.category_pattern = category_pattern
        self.categoryDict.update(extra_cat_dict)
        self.start_date = start_date
        self.end_date = end_date
        self.num_days = (end_date - start_date).days

    def parse(self, response):
        one_day = datetime.timedelta(days=1)

        for base_url in self.base_urls:
            current_date = self.start_date
            for i in range(0, self.num_days + 1):
                url = base_url + current_date.strftime('%Y-%m-%d') + "/"
                print(url)
                current_date += one_day
                yield scrapy.Request(url, callback=self.parse_date_page, dont_filter=True)

    def parse_date_page(self, response):
        links = response.xpath(self.href_pattern)
        for href in links:
            if href.extract().find('javascript') == -1:
                url = self.start_urls[0] + href.extract()
                yield scrapy.Request(url, callback=self.parse_news_contents, dont_filter=True)

    def parse_title(self, response, xpath_pattern):
        title = ''
        titles = response.xpath(xpath_pattern).extract()
        if len(titles) > 0:
            for str in titles:
                if len(str.strip()) > 0:
                    title = str.strip().lower()
                    break
        return title

    def parse_summary(self, response, xpath_pattern):
        summary = ''
        summaries = response.xpath(xpath_pattern).extract()
        if len(summaries) != 0:
            summaries = [x.strip() for x in summaries if len(x.strip()) > 0]
            summary = " ".join(summaries).lower()

        return summary

    def parse_tags(self, response, xpath_pattern):
        tagstr = ''
        tags = response.xpath(xpath_pattern).extract()
        if len(tags) != 0:
            tagstr = ",".join([tag.strip().lower() for tag in tags])
        else:
            tagstr = ""

        return tagstr

    def parse_categories(self, response, xpath_pattern):
        catStr = ''
        categories = response.xpath(xpath_pattern).extract()
        if len(categories) > 0:
            catStr = self.categoryDict.get(categories[0].strip().lower(), '')
            if len(categories) > 1:
                cat = self.categoryDict.get(categories[1].strip().lower(), '')
                if cat != '':
                    catStr = cat

        return catStr

    def parse_paragraphs(self, response, xpath_pattern):
        paraStr = ''
        paragraphs = response.xpath(xpath_pattern).extract()
        if len(paragraphs) != 0:
            paragraphs = [x.strip() for x in paragraphs if len(x.strip()) > 0]
            paraStr = " ".join(paragraphs).lower()

        return paraStr

    def parse_news_contents(self, response):
        item = NewsItem()

        item['text'] = self.parse_paragraphs(response, self.text_pattern)
        if len(item['text']) != 0:
            item['title'] = self.parse_title(response, self.title_pattern)
            item['summary'] = self.parse_summary(response, self.summary_pattern)
            item['text'] = item['title'] + ". " + item['text']
            item['tags'] = self.parse_tags(response, self.tag_pattern)
            item['category'] = self.parse_categories(response, self.category_pattern)
            item['url'] = response.url

            yield item



