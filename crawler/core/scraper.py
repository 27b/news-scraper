from abc import ABC, abstractmethod
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from datetime import datetime as dt
from re import compile


class IScraper(ABC):
    """Wrap the scraping module to keep a minimum coupling."""

    @abstractmethod
    def execute(self, url: str, values: dict, category: str) -> list[dict]:
        """Execute the scraper with config and returns the result."""
        pass


class AutoScraperScraper(IScraper):
    """Interface of AutoScraper module."""

    @classmethod
    def execute(cls, url: str, values: dict, category: str) -> list[dict]:
        """Execute the Scrapy scraper with config and returns the result.

        Args:
            url: The url that the scraper will receive.
            values: Addresses of html elements.
            category: An string to be inserted in each dict of the list.

        Returns:
            A list of dictionaries with title, description, author,
            datetime and category.
        """
        scraper = SimpleScrapyScraper
        scraper.name = 'AutoScraper'
        scraper.start_urls = [url]
        scraper.values = values
        scraper.category = category
        process = CrawlerProcess()
        process.crawl(scraper)
        return process.start()


class SimpleScrapyScraper(Spider):
    """Simple wraper of Scrapy."""
    
    @staticmethod
    def parse(response) -> list[dict]:
        post = response.css('div.css-13mho3u ol')
        title = post.css('li div div a h2::text').getall()
        description = post.css('li div div a p.css-1echdzn::text').getall()
        author = post.css('li div div a div.css-1nqbnmb.e140qd2t0 p').getall()
        return [
            {
                'title': post[0],
                'description': post[1],
                'author': compile(r'<[^>]+>').sub('', post[2]).split('By ')[1],
                'datetime': dt.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }
            for post in list(zip(title, description, author))
        ]
