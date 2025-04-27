import scrapy
from SpiderHouse.items import SpiderhouseItem

class RentolaSpider(scrapy.Spider):
    name = "Rentola"
    domains = "https://rentola.pt"
    data = {}

    def start_requests(self):
        yield scrapy.Request(
            url=self.domains ,
            method="GET",
            callback=self.category
        )
    
    def category(self, response):
        for get_link in response.xpath('//div[@class="flex mb-2 w-max gap-4"]/a/@href').getall():
            link = self.domains + get_link
            yield scrapy.Request(
                url=link,
                method="GET",
                callback=self.parse
            )

    def request_page(self,url):
        yield scrapy.Request(
            url=url,
            method="GET",
            callback=self.parse
               )

    def parse(self, response):
        for get_link in response.xpath('//div[@class="relative flex h-full flex-col overflow-hidden rounded-3xl border border-grey-300"]/div[@class="relative h-full bg-white p-4"]/a/@href').getall():
            link = self.domains + get_link
            yield scrapy.Request(
                url=link,
                method="GET",
                callback=self.collecting_data
            )
        yield from self.page(response)

    def collecting_data(self, response):
        self.data["Title"] = response.xpath('//div[@class="xl:col-span-9"]/h1[@class="text-[32px] font-bold"]/text()').get()
        self.data["Location"] = response.xpath('//div[@class="xl:col-span-9"]/a/p/text()').get()
        self.data["Price"] = response.xpath('//div[@class="sticky top-20"]/div/p[@class="mb-6 text-[32px] font-bold"]/text()').get()
        self.data["Property_Type"] = response.xpath('//div[@class="flex justify-between rounded-xl border border-grey-200 bg-grey-100 p-4"]/p[@class="text-sm font-[400]"]/text()').get()
        self.data["Rooms"] = response.xpath('//div[@class="flex justify-between rounded-xl border border-grey-200 bg-grey-100 p-4"][2]/p[@class="text-sm font-[400]"]/text()').get()
        self. data["Size"] = response.xpath('//div[@class="flex justify-between rounded-xl border border-grey-200 bg-grey-100 p-4"][3]/p[@class="text-sm font-[400]"]/text()').get()
   
        yield SpiderhouseItem(
            self.data
        )
    
    def page(self, response):
        next_page = response.xpath('//div[@role="navigation"]/a[2]/@href').get()
        if next_page:
            new_page = self.domains + next_page
            yield from self.request_page(new_page)