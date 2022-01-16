from abc import ABC,  abstractmethod

from crawler.core.scraper import IScraper


class ISpider(ABC):
    """High Abstraction of the library of scraping."""

    @abstractmethod
    async def execute_scraper(self, newsletter: dict) -> None:
        """Run the low level abstraction of the scraper library."""
        pass

    @abstractmethod
    def result(self) -> list[dict]:
        """Get the result of the object."""
        pass


class BasicSpider(ISpider):
    """Return a list of four values per dict."""

    def __init__(self, scraper: IScraper):
        self.scraper = scraper
        self.results_of_categories = None

    def execute_scraper(self, newsletter: dict) -> None:
        """Run the low level abstraction of the scraper library."""
        result = None

        for category in newsletter['categories']:
            print(f'Category: {category}')
            for url in newsletter['categories'][category]:
                print(f' * URL: {url}')
                wanted_list = newsletter['wanted_list']
                page = self.scraper.execute(url, wanted_list, category)
                result = page
        self.results_of_categories = result

    def result(self) -> list[dict]:
        return self.results_of_categories
