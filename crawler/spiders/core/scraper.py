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

    async def execute(self, url: str, values: dict, category: str) -> list[dict]:
        """Execute AutoScraper with the config and returns the result."""
        scraper = AutoScraper()
        await scraper.build(url, wanted_dict=values)

        # group and organize results
        v = await scraper.get_result_similar(
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
