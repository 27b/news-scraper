from crawler.spiders.core.spider import BasicSpider
from crawler.spiders.core.scraper import AutoScraperScraper
from config import list_of_sites
from time import sleep
from models import Post, Category


TIME_FOR_SLEEP = 60 * 1
SCRAPER_LIST = list_of_sites


class Crawler:
    """Execute multiple spiders and insert the results in the database."""
    __database_instance = None

    @classmethod
    def __insert_in_database(cls, name: str, list_of_posts: list[dict]) -> None:
        """Insert the new values in the database."""
        if cls.__database_instance:
            db = cls.__database_instance
            for post in list_of_posts:
                newsletter_in_db = Newslette.query.filter_by(name=name).first()
                category_in_db = Category.query.filter_by(title=post.category).first()
                post_in_db = Post.query.filter_by(title=post.title)
                if newsletter_in_db and category_in_db and not post_in_db:
                    try:
                        new_post = Post()
                        new_post.title = post['title']
                        new_post.description = post['description']
                        new_post.author = post['author']
                        new_post.url = post['url']
                        new_post.newsletter_id = newsletter_in_db.id
                        new_post.category_id = category_in_db.id
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
                cls.__insert_in_database(newsletter.name, spider.result())
