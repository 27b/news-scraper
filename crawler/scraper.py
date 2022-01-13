from time import sleep
from spiders.nytimes import NYTimesScraper

TIME_FOR_SLEEP = 60*1


class Crawler:
    """Execute multiple spiders and insert the results in the database."""
    database = None

    @classmethod
    def __insert_in_database(cls) -> None:
        """Insert the new values in the database."""

    @classmethod
    def run_task(cls, database) -> None:
        """
        Run this method in a background task, this method execute the scrapers
        and send data in cls, this data is inserted in the database.
        """
        cls.database = database
        while True:
            sleep(TIME_FOR_SLEEP)
            # Task
