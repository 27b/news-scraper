from abc import ABC, abstractmethod
from scrapy import Spider, signals, http
from scrapy.crawler import CrawlerProcess
from datetime import datetime as dt
from re import compile
import logging


logging.getLogger('scrapy').propagate = False


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
            result = scraper.result
        except Exception as error:
            print('SCRAPER ERROR', error)
        else:
            queue.put(result)


class SimpleScrapyScraper(Spider):
    """Simple wrapper of Scrapy."""
    name = 'SimpleScraperUsingScrapy'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    result = []

    @classmethod
    def parse(cls, response) -> None:
        try:
            container = response.css(cls.values['container'])
            for content in container:
                title = content.css(cls.values['title']).get()
                description = content.css(cls.values['description']).get()

                author_list = content.css(cls.values['author']).getall()    
                author_quantity = len(author_list) 

                if author_quantity == 1:
                    author = str(content.css(cls.values['author']).get())    
                if author_quantity > 1:
                    author = ''
                    for index, person in enumerate(author_list, start=1):
                        if index != author_quantity:
                            person += ' and'
                        author += f' {person}'
                else:
                    author = '' # NoneType (Not HTML)

                author = compile(r'<[^>]+>').sub('', author)

                if 'By' in author:
                    author = author.split('By')[1].strip()
                
                post = {
                    'title': title.strip(),
                    'description': description.strip(),
                    'author': author,
                    'datetime': dt.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    'category': cls.category
                }
                print(post)
                cls.result.append(post)

        except Exception as error:
            print('SCRAPY ERROR', error)
