from abc import ABC, abstractmethod
from autoscraper import AutoScraper


class IScraper(ABC):
    """Wrap the scraping module to keep a minimum coupling."""

    @abstractmethod
    def execute(self, url: str, values: dict, category: str) -> list[dict]:
        """Execute the scraper with config and returns the result."""
        pass


class AutoScraperScraper(IScraper):
    """Interface of AutoScraper module."""

    def execute(self, url: str, values: dict, category: str) -> list[dict]:
        """Execute the AutoScraper with config and returns the result.

        Note:
            AutoScraper don't have documentation, that is why it is
            difficult to use the library, for now the performance is not very
            good due to how the data must be organized.

        Args:
            url: The url that the scraper will receive.
            values:
            category: An string to be inserted in each dict of the list.

        Returns:
            A list of dictionaries with title, description, author and
            category.
        """
        scraper = AutoScraper()
        scraper.build(url, wanted_dict=values)

        # group and organize results
        v = scraper.get_result_similar(
            url, keep_order=True, grouped=True, group_by_alias=True
        )

        # Separate results
        r_zip = list(zip(v['title'], v['description'], v['author']))

        result = [
            {
                'title': i[0],
                'description': i[1],
                'author': i[2],
                'category': category
            }
            for i in r_zip
        ]

        return result
