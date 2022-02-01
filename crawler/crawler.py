from crawler.config import list_of_sites
from crawler.core.scraper import AutoScraperScraper
from crawler.core.spider import BasicSpider
from models import Newsletter, Category, Post
from time import sleep


TIME_FOR_SLEEP = 60 * 1
SCRAPER_LIST = list_of_sites


class Crawler:
    """Execute multiple spiders and insert the results in the database."""
    __database_instance = None

    @classmethod
    def __insert_in_database(cls, name: str, list_of_posts: list[dict]) -> None:
        """Insert the new values in the database.

        Args:
            name: The Newsletter name, is used to search using Newsletter model.
            list_of_posts: List of rules, stay in the file: config.py.

        Returns:
            Run permanently.
        """
        if cls.__database_instance:
            db = cls.__database_instance
            for post in list_of_posts:
                # Optimize this by storing the category/newsletter values in the class
                # and accessing them instead of making constant requests to the database.
                newsletter_in_db = Newsletter.query.filter_by(name=name).first()
                category_in_db = Category.query.filter_by(name=post.get('category')).first()
                post_in_db = Post.query.filter_by(title=post.get('title')).first()
                if newsletter_in_db and category_in_db:
                    if not post_in_db:
                        try:
                            new_post = Post()
                            new_post.title = post.get('title')
                            new_post.description = post.get('description')
                            new_post.author = post.get('author')
                            new_post.url = post.get('url')
                            new_post.newsletter_id = newsletter_in_db.id
                            new_post.category_id = category_in_db.id
                            db.session.add(new_post)
                            db.session.commit()
                        except Exception as e:
                            print(f'ERROR: {e}')
                    else:
                        pass  # Post already in database
                else:
                    print(f'ERROR: Newsletter with de name {name} not in database.')
        else:
            print('ERROR: Database not instanced.')

    @classmethod
    def run_task(cls, database) -> None:
        """Run this method in a background task, this method execute the
        scrapers and send data in cls, this data is inserted in the database.
        """
        cls.__database_instance = database

        while True:
            sleep(TIME_FOR_SLEEP)
            for newsletter in SCRAPER_LIST:
                # Execute subprocess
                print(f"RUN: {newsletter['name']}")
                spider = BasicSpider(AutoScraperScraper())
                spider.execute_scraper(newsletter)
                result = spider.result()
                if result is not None:
                    cls.__insert_in_database(newsletter['name'], result)
                else:
                    print(f"ERROR: The result of {newsletter['name']} is: {result}")
