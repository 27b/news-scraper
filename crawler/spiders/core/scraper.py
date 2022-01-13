from autoscraper import AutoScraper


class IScraper:
    """Wrap the scraping module to keep a minimum coupling."""

    def __init__(self, url: str, values: list[str]):
        self.url = url
        self.values = values

    def execute(self) -> list[dict]:
        """Execute the scraper with config and returns the result."""
        raise NotImplementedError


class AutoScraper(IScraper):
    """Interface of AutoScraper module."""

    def execute(self) -> list[dict]:
        """ Execute the e"""
        scraper = AutoScraper()
        result = scraper.build(self.url, self.values)
        return result
