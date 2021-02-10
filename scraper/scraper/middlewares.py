import os
import random
from scrapy.conf import settings
import base64

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua  = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)
        request.headers.setdefault('apikey', '2cd335e2c2c74a6f9f4b540b91128e55')

class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        hp = random.choice(settings.get('HTTP_PROXY'))
        if hp:
            request.meta['proxy'] = hp
            # proxy_user_pass = "USERNAME:PASSWORD"
            # encoded_user_pass = base64.encodestring(proxy_user_pass)
            # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass