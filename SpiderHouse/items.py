import scrapy

class SpiderhouseItem(scrapy.Item):
    Title = scrapy.Field()
    Location = scrapy.Field()
    Price = scrapy.Field()
    Property_Type = scrapy.Field()
    Rooms = scrapy.Field()
    Size = scrapy.Field()
    