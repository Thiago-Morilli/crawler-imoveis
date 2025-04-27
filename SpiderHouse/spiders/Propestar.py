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
    
    def parse(self, response):
        get_link = response.xpath('//div[@class="item-data"]/a[@class="link listing-title stretched-link"]/@href').get()
        link = self.domains + get_link
        yield scrapy.Request(
            url=link,
            method="GET",
            callback=self.properties
        )       


    def properties(self, response):
        self.data["Tilte"] = response.xpath('//section[@class="item-intro"]/div/h1/text()').get()
        self.data["Price"] = response.xpath('//div[@class="listing-price-main"]/span/text()').get().replace("\xa0€", "")
        self.data["location"] = response.xpath('//div[@class="address"]/span/text()').get()
        print(self.data)
        