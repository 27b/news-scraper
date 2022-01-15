from crawler.spiders.core.spider import BasicSpider
from crawler.spiders.core.scraper import AutoScraperScraper
from config import list_of_sites
from time import sleep
from models import Post


TIME_FOR_SLEEP = 60 * 1
SCRAPER_LIST = list_of_sites


class Crawler:
    """Execute multiple spiders and insert the results in the database."""
    __database_instance = None

    @classmethod
    def __insert_in_database(cls, list_of_posts: list[dict]) -> None:
        """Insert the new values in the database."""
        if cls.__database_instance:
            db = cls.__database_instance
            for post in list_of_posts:
                post_in_db = db.query.filter_by(title=post.title)
                if not post_in_db:
                    try:
                        new_post = Post()
                        new_post.title = post.title
                        new_post.description = post.description
                        new_post.content = post.content
                        new_post.url = post.url
                        db.session.add(new_post)
                        db.session.commit()
                    except Exception as e:
                        print(f'ERROR: {e}')
        else:
            print('ERROR: Database not instanced.')

    @classmethod
    def run_task(cls, database) -> None:
        """
        Run this method in a background task, this method execute the scrapers
        and send data in cls, this data is inserted in the database.
        """
        __database_instance = database

        while True:
            sleep(TIME_FOR_SLEEP)
            # Run subprocess
            for newsletter in SCRAPER_LIST:
                # Execute subprocess
                spider = BasicSpider(AutoScraperScraper())
                spider.execute_scraper(newsletter)
                cls.__insert_in_database(spider.result())
