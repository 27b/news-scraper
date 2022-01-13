# PROBLEMS TO RESOLVE
# 1. Low coupling with the scraping library
# 2. Create a Mixin that can use the low coupling class and get the data

from scraper import IScraper


class ISpider:
    """High Abstraction of the library of scraping."""

    def __init__(self, scraper: IScraper):
        self.scraper = scraper
        self.result = None

    async def execute_scraper(self, url: str, values: list[str]) -> None:
        """Run the low level abstraction of the scraper library."""
        raise NotImplementedError

    async def get_result(self) -> list[dict]:
        """Get the result of the object."""
        raise NotImplementedError


class BasicSpider(ISpider):
    """Return a list of four values per dict."""

    async def execute_scraper(self, url: str, values: list[str, str, str]):
        pass

    async def get_result(self):
        pass
