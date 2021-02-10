import scrapy
from scraper.items import TikieListItems
class TikiNet(scrapy.Spider):
    name = "tiki"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ProductTikiPipeline.ProductTikiPipeline': 310
        }
    }
    def start_requests(self):
        urls = [
            'https://tiki.vn/dien-thoai-may-tinh-bang/c1789?page=9'
            # 'https://tiki.vn/thiet-bi-kts-phu-kien-so?src=mega-menu'
            # 'https://sohoa.vnexpress.net/tin-tuc/doi-song-so/tap-chi-co-chu-ky-steve-jobs-duoc-ban-gia-50-000-usd-3662652.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_tiki)

    def parse_tiki(self, response):
        # artilce = {}
        # artilce['title'] = response.xpath('//*[@id="col_sticky"]/h1/text()').extract()[0].encode('utf-8').strip()
        # artilce['description'] = response.xpath('//*[@id="col_sticky"]/h2/text()').extract()[0].encode('utf-8').strip()
        # artilce['content'] = response.xpath('//*[@id="col_sticky"]/article').extract()[0].encode('utf-8').strip()
        # artilce['author'] = response.xpath('//*[@id="col_sticky"]/article/p[5]/strong/text()').extract()[0].encode('utf-8').strip()
        # artilce['publish_date'] = response.xpath('//*[@id="col_sticky"]/header/span/text()').extract()[0].encode('utf-8').strip()
        # for key, text in artilce.iteritems():
        #     print("{key}: {text}".format(key = key.upper(), text = text))
        # filename = response.url.split("/")[-1] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        questions = response.css('div.product-item')
        for question in questions:
            review = question.css('.review::text')
            if (len(review) == 0):
                continue
            item = TikieListItems()
            item['product_id'] = question.css('a::attr(data-id)').extract()[0]
            item['review'] = review.extract()[0]
            # item['link'] = question.css('a::attr(href)').extract()[0]
            yield item