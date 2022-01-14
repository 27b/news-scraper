from time import sleep
from config import CONFIG

TIME_FOR_SLEEP = 60 * 1
SCRAPER_LIST = CONFIG


class Crawler:
    """Execute multiple spiders and insert the results in the database."""
    database_instance = None

    @classmethod
    def __insert_in_database(cls) -> None:
        """Insert the new values in the database."""
        if cls.database_instance:
            try:
                pass
            except Exception as e:
                print(e)
        else:
            print('ERROR: Database not instanced.')

    @classmethod
    def run_task(cls, database) -> None:
        """
        Run this method in a background task, this method execute the scrapers
        and send data in cls, this data is inserted in the database.
        """
        cls.database_instance = database
        while True:
            sleep(TIME_FOR_SLEEP)
            # Run subprocess
            for index, newsletter in SCRAPER_LIST:
                # Execute subprocess
                pass
