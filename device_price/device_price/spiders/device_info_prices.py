import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from device_price.items import DevicePriceItem


class Device_and_prices(scrapy.Spider):
    name = 'Device_and_prices'
    start_urls = ['https://orangebookvalue.com/used-mobiles']
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    base_url = 'https://orangebookvalue.com'
    # options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install())

    def start_requests(self):
        # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.links)

    def links(self, response):
        links = response.css('.content.text-center a ::attr(href)').getall()
        for url in links:
            yield scrapy.Request(self.base_url + url, headers=self.headers, callback=self.mobile_models)

    def mobile_models(self, response):
        products = response.css('.content.text-center a ::attr(href)').getall()
        for product in products:
            yield scrapy.Request(self.base_url + product, headers=self.headers, callback=self.parse)

    def excellent_condition(self, response):
        self.driver.get(response.url)
        next = self.driver.find_element_by_xpath('//*[@id="home"]/div[4]/div[1]/div/div/div[3]/ul/li[5]/a')
        next.click()
        self.driver.implicitly_wait(30)
        source = self.driver.page_source  # get source of the loaded page
        sel = Selector(text=source)  # create a Selector object
        range = sel.css('.price > span.range_from ::text').extract()
        to = sel.css('.price > span.range_to ::text').extract()
        return range, to

    def parse(self, response):
        name_of_device_and_model = response.css('.page-header h1 ::text').get()
        lowest_price = response.css('.price > span.range_from ::text').get()
        max_price = response.css('.price > span.range_to ::text').get()
        brand = name_of_device_and_model.split()[1]
        model = name_of_device_and_model.split()[2:-1]
        model_name = " ".join(model)
        result = self.excellent_condition(response)
        item = DevicePriceItem()
        item['brand'] = brand
        item['model'] = model_name
        item['lowest_price'] = lowest_price.split()[1]
        item['maximum_price'] = max_price.split()[2]
        item['excellent_lowest'] = str(result[0][0]).split()[-1]
        item['excellent_maximum'] = str(result[1][0]).split()[-1]
        # print(str(result[0][0]).split()[-1], str(result[1][0]).split()[-1])
        # yield {
        #     'brand': brand,
        #     'model': model_name,
        #     'lowest_price': lowest_price.split()[1],
        #     'maximum_price': max_price.split()[2],
        #     'excellent_lowest': str(result[0][0]).split()[-1],
        #     'excellent_maximum': str(result[1][0]).split()[-1]
        # }
        yield item
