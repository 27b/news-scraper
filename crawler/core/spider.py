from abc import ABC,  abstractmethod
from crawler.core.scraper import IScraper
from multiprocessing import Process, Queue


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
    """Access each category of the newsletter and in each category access each
    item, within each item you access the link using the provided scraper and
    the result is stored, you can access it using result method.
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
        result = []
        result_of_process = Queue()
        for category in newsletter['categories']:
            for item in newsletter['categories'][category]:
                case = item['case']
                wanted_list = newsletter['wanted_list'][case]
                if wanted_list:
                    result_of_page = Process(
                        target=self.scraper.execute,
                        args=(result_of_process, item.get('url'), wanted_list, category)
                    )
                    print(f"Starting {newsletter['name']} - {category}")
                    result_of_page.start()
                    result_of_page.join()
                else:
                    print(f"ERROR: {case} not in the wanted list of {newsletter.get('name')}.")
        while result_of_process.empty() is False:
            process_result = result_of_process.get()
            result.extend(process_result)
            print('RESULT SAVED.')
        self.results_of_categories = result if result != [] else None

    def result(self) -> list[dict]:
        """Return the results of the scraper.

        Returns
            A list of dictionaries.
        """
        return self.results_of_categories
