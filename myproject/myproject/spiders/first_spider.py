# first_spider.py
import scrapy

class FirstSpider(scrapy.Spider):
    name = "firstspyder"
    start_urls = ['https://www.bajajelectronics.com/']  # Add relevant URLs

    def parse(self, response):
        # Extract all text elements from the body
        all_text = response.xpath('//body//text()').getall()  # Get all text nodes in the body

        # Clean and join the text
        cleaned_text = ' '.join([text.strip() for text in all_text if text.strip()])  # Remove extra whitespace
        print(cleaned_text)

        # Yield the cleaned text
        yield {
            'text': cleaned_text
        }

        # Follow pagination links if necessary
        next_page = response.xpath('//a[contains(@class, "next-page")]/@href').get()  # Update the XPath for the next page link
        if next_page:
            yield response.follow(next_page, self.parse)
