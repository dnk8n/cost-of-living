import scrapy


class CitySpider(scrapy.Spider):
    name = 'cost_of_living'
    allowed_domains = ['numbeo.com']
    start_urls = ['https://www.numbeo.com/cost-of-living/country_result.jsp?country={}'.format(c) for c in ['Indonesia', 'Western+Sahara', 'Yemen', 'Zambia']]

    def parse(self, response):
        country = response.url.split('=')[1]
        rows = response.xpath('/html/body/div[2]/div[6]/table/tbody/tr')
        for row in rows:
            import ipdb; ipdb.set_trace()
            rank = row.xpath('./td[1]/text()').get()
            city = row.xpath('./td[2]/a/text()').get()
            cost_of_living_index = row.xpath('./td[3]/text()').get()
            rent_index = row.xpath('./td[4]/text()').get()
            restaurant_price_index = row.xpath('./td[5]/text()').get()
            yield {
                'country': country,
                'rank': rank,
                'city': city,
                'cost_of_living_index': cost_of_living_index,
                'rent_index': rent_index,
                'restaurant_price_index': restaurant_price_index,
            }
