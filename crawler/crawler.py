from crawler.config import list_of_sites
from crawler.core.scraper import AutoScraperScraper
from crawler.core.spider import BasicSpider
from models import Newsletter, Category, Post
from time import sleep


TIME_FOR_SLEEP = 60 * 1
SCRAPER_LIST = list_of_sites


class Crawler:
    """Execute multiple spiders and insert the results in the database."""
    __database = None
    __categories = None
    __newsletters = None

    @classmethod
    def __insert_in_database(cls, name: str, list_of_posts: list[dict]) -> None:
        """Insert the new values in the database.

        Args:
            name: The Newsletter name, is used to search using Newsletter.
            list_of_posts: List of rules, stay in the file: config.py.

        Returns:
            Run permanently.
        """
        if not cls.__newsletters:
            cls.__newsletters = [M for M in Newsletter.query.all()]
            print('Newsletter list created:', cls.__newsletters)
        if not cls.__categories:
            cls.__categories = [M for M in Category.query.all()]
            print('Categories list created:', cls.__categories)
        if cls.__database:
            db = cls.__database
            for post in list_of_posts:
                category = post.get('category')
                newsletter_in_db = list(filter(lambda x: x.name == name, cls.__newsletters))
                category_in_db = list(filter(lambda x: x.name == category, cls.__categories))
                post_in_db = Post.query.filter_by(title=post.get('title')).first()
                try:
                    if category_in_db == []:
                        print('ERROR: Category does not exist.')
                    elif newsletter_in_db[0] and category_in_db[0]:
                        if not post_in_db:
                            new_post = Post()
                            new_post.title = post.get('title')
                            new_post.description = post.get('description')
                            new_post.author = post.get('author')
                            new_post.url = post.get('url')
                            new_post.newsletter_id = newsletter_in_db[0].id
                            new_post.category_id = category_in_db[0].id
                            db.session.add(new_post)
                            db.session.commit()
                        else:
                            pass  # Post already in database
                    else:
                        print(f'ERROR: Newsletter {name} not in database.')
                except Exception as e:
                    print(f'ERROR: {e}')
        else:
            print('ERROR: Database not instanced.')

    @classmethod
    def run_task(cls, database) -> None:
        """Run this method in a background task, this method execute the
        scrapers and send data in cls, this data is inserted in the database.
        """
        cls.__database = database

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
