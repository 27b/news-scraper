from abc import ABC, abstractmethod

from autoscraper import AutoScraper


class IScraper(ABC):
    """Wrap the scraping module to keep a minimum coupling."""

    @abstractmethod
    def execute(self, url: str, values: list[str]) -> list[dict]:
        """Execute the scraper with config and returns the result."""
        pass


class AutoScraperScraper(IScraper):
    """Interface of AutoScraper module."""

    async def execute(self, url: str, values: list[str]) -> list[dict]:
        """
        :param url: string
        :param values: wanted resources
        :return: dict wi
        """
        scraper = AutoScraper()
        result = await scraper.build(self.url, self.values)
        return result  # {title:, description:, content:, datetime:}
