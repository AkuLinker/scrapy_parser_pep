import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['http://peps.python.org/']

    def parse(self, response):
        peps = response.css('section#numerical-index tbody tr')
        for pep_url in peps.css('td.num a::attr(href)'):
            yield response.follow(pep_url, callback=self.parse_pep)

    def parse_pep(self, response):
        h1 = response.css('h1.page-title::text').get().strip()
        number_of_pep, name_of_pep = re.split(' – ', h1)
        data = {
            'number': number_of_pep.replace('PEP ', ''),
            'name': name_of_pep,
            'status': response.css('dt:contains("Status") + dd::text').get(),
        }
        yield PepParseItem(data)
