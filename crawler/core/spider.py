from abc import ABC,  abstractmethod
from crawler.core.scraper import IScraper


class ISpider(ABC):
    """High Abstraction of the library of scraping."""

    @abstractmethod
    def execute_scraper(self, newsletter: dict) -> None:
        """Run the low level abstraction of the scraper library."""
        pass

    @abstractmethod
    def result(self) -> list[dict]:
        """Get the result of the object."""
        pass


class BasicSpider(ISpider):
    """
    Access each category of the newsletter and in each category
    access each item. Within each item you access the link using
    the provided scraper and the result is stored, you can access
    it using result method.
    """

    def __init__(self, scraper: IScraper):
        self.scraper = scraper
        self.results_of_categories = None

    def execute_scraper(self, newsletter: dict) -> None:
        """Run the low level abstraction of the scraper library.

        Args:
            newsletter: receive a dictionary of the config file.

        Returns:
            None, to get the result execute the result method.
        """
        result = None
        for category in newsletter['categories']:
            for item in newsletter['categories'][category]:
                case = item.get('case')
                wanted_list = category['wanted_list'][case]
                if wanted_list: 
                    page = self.scraper.execute(item.get('url'), wanted_list, category)
                    result = page
                else:
                    print(f"ERROR: {case} not in the wanted list of { newsletter.get('name') }.")
        self.results_of_categories = result

    def result(self) -> list[dict]:
        """Return the results of the scraper.

        Returns
            A list of dictionaries.
        """
        return self.results_of_categories
