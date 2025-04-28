import scrapy

class PropestarSpider(scrapy.Spider):
    name = "Propestar"
    domains = "https://www.properstar.pt"
    search = "/portugal/alugar/apartamento-casas?price.max=600000"
    data = {}

    def start_requests(self):
        yield scrapy.Request(
            url=self.domains + self.search,
            method="GET",
            callback=self.parse
        )

    def request_page(self, url):
        yield scrapy.Request(
            url=url,
            method="GET",
            callback=self.parse
        )

    def parse(self, response):
        for get_link in response.xpath('//div[@class="item-data"]/a[@class="link listing-title stretched-link"]/@href').getall():
            link = self.domains + get_link
            yield scrapy.Request(
                url=link,
                method="GET",
                callback=self.properties
            )       

        yield from self.pagination(response)

    def properties(self, response):
        self.data["Tilte"] = response.xpath('//section[@class="item-intro"]/div/h1/text()').get()
        self.data["Price"] = response.xpath('//div[@class="listing-price-main"]/span/text()').get().replace("\xa0€", "")
        self.data["location"] = response.xpath('//div[@class="address"]/span/text()').get()
        self.data["Rooms"] = response.xpath('//div[@class="feature-item"][2]/div/span[@class="property-value"]/text()').get()
        self.data["Property_Type"] = response.xpath('//div[@class="secondary-info"]/div[@class="item-highlights"]/text()').get().split("•")[0]
        self.data["size"] = response.xpath('//div[@class="feature-list property-list"][2]/div/div/span[@class="property-value"]/text()').get()



    def pagination(self, response):
        page = response.xpath('//div[@class="pagination"]/ul/li[@class="page-link next"]/a/@href').get() 
        if page:
            link = self.domains + page
            yield from self.request_page(link)
            