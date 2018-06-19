import scrapy
import re
from scrapy.linkextractors import LinkExtractor

class RCOUCFMFSpider(scrapy.Spider):
	name = "rcoucfmf"
	start_urls = [
		'http://www.rcuocfmf.com/',
	]

	url_matcher = re.compile('\http\:\/\/www\.rcuocfmf\.com\/search\/label\/')

	def parse(self, response):
		link_extractor = LinkExtractor(allow=RCOUCFMFSpider.url_matcher)
		links = [link.url for link in link_extractor.extract_links(response)]

		for link in links:
			yield scrapy.Request(url=link, callback=self.parse_articles)

	def parse_articles(self,response):
		
		post_links = response.css('div.post-outer div.post article div.post-home div.post-info h2.post-title a::attr(href)').extract()	
		
		for post_link in post_links:
			yield scrapy.Request(url=post_link, callback=self.extract_info)

	def extract_info(self,response):
		yield {
			'url' : response.url,
			'name': response.css('div.post-header div.post-heading h1.post-title.entry-title::text').extract_first(),
			'category': response.css('div.post-outer div.post div div.post-header div.breadcrumbs span a::text').extract(),
			'content': response.css('div div.separator').extract(),
			'date': response.css('div.post-outer div.post div div.post-header div.post-meta span.post-timestamp a.timestamp-link').extract()
		}