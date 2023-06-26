from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor 

class toscrape(CrawlSpider): 
    name = "toscrape" 
    allowed_domains =  [ "toscrape.com" ]
    start_urls = [ "http://books.toscrape.com/" ]    
    rules = (
        Rule(LinkExtractor(allow="catalogue/category")),
        Rule(LinkExtractor(allow="catalogue", deny="category"), callback="parse_item"),
    )
    
    def parse_item(self, response): 
        yield {
            "title": response.css(".product_main h1::text" ).get(),
            "price": response.css(".price_color::text").get(),
            "descripton": response.css(".product_page p::text")[10].get(),
            "image": response.css(".item.active img::attr(src)").get()
        }
    
    