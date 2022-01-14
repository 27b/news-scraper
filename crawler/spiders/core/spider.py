from abc import ABC,  abstractmethod

from scraper import IScraper


class ISpider(ABC):
    """High Abstraction of the library of scraping."""

    @abstractmethod
    async def execute_scraper(self, newsletter: dict) -> None:
        """Run the low lev el abstraction of the scraper library."""
        pass

    @abstractmethod
    def result(self) -> list[dict]:
        """Get the result of the object."""
        pass


class BasicSpider(ISpider):
    """Return a list of four values per dict."""

    def __init__(self, scraper: IScraper):
        self.scraper = scraper
        self.result = None

    async def execute_scraper(self, newsletter: dict) -> None:
        """
        :param newsletter:
        :return:
        """
        result = []
        for category in newsletter['categories']:
            for url in category:
                wanted_list = newsletter['wanted_list']
                scraped_page = await self.scraper.execute(url, wanted_list)
                scraped_page['category'] = category
                result.append(scraped_page)
        self.result = result

    def result(self) -> list[dict]:
        return self.result
