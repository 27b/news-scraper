from abc import ABC, abstractmethod
from scrapy import Spider, signals
from scrapy.crawler import CrawlerProcess
from datetime import datetime as dt
from re import compile
import logging


logging.getLogger('scrapy').setLevel(logging.WARNING)


class IScraper(ABC):
    """Wrap the scraping module to keep a minimum coupling."""

    @abstractmethod
    def execute(self, queue, url: str, values: dict, category: str) -> None:
        """Execute the scraper with config and returns the result."""
        pass


class AutoScraperScraper(IScraper):
    """Interface of AutoScraper module."""

    @classmethod
    def execute(cls, queue, url: str, values: dict, category: str) -> None:
        """Execute the Scrapy scraper with config and returns the result.

        Args:
            queue: A queue of multiprocessing.
            url: The url that the scraper will receive.
            values: Addresses of html elements.
            category: An string to be inserted in each dict of the list.

        Returns:
            A list of dictionaries with title, description, author,
            datetime and category.
        """
        try:
            scraper = SimpleScrapyScraper
            scraper.start_urls = [url]
            scraper.values = values
            scraper.category = category
            process = CrawlerProcess()
            process.crawl(scraper)
            process.start()  # Don't use exceptions, let it crash
            r = scraper.result
        except Exception as error:
            print('SCRAPER ERROR', error)
        else:
            queue.put(r)


class SimpleScrapyScraper(Spider):
    """Simple wrapper of Scrapy."""
    name = 'SimpleScraperUsingScrapy'

    @classmethod
    def parse(cls, response) -> None:
        try:
            post = response.css(cls.values['container'])
            title = post.css(cls.values['title']).getall()
            description = post.css(cls.values['description']).getall()
            author = post.css(cls.values['author']).getall()
            cls.result = [
                {
                    'title': post[0],
                    'description': post[1],
                    'author': compile(r'<[^>]+>').sub('', post[2]).split('By ')[1],
                    'datetime': dt.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    'category': cls.category
                }
                for post in list(zip(title, description, author))
            ]
        except Exception as error:
            print('SCRAPY ERROR', error)
