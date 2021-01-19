# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DevicePriceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    lowest_price = scrapy.Field()
    maximum_price = scrapy.Field()
    excellent_lowest = scrapy.Field()
    excellent_maximum = scrapy.Field()
