from crawler.config import list_of_sites
from crawler.core.scraper import AutoScraperScraper
from crawler.core.spider import BasicSpider
from models import Newsletter, Category, Post
from time import sleep
from sys import exit


TIME_FOR_SLEEP = 2 * 5
SCRAPER_LIST = list_of_sites


class Crawler:
    """Execute multiple spiders and insert the results in the database."""
    __app = None
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
            None.
        """
        try:
            if not cls.__app or not cls.__database:
                msg = "The application or database has not been instantiated."
                print('ERROR:', msg)
                exit()
            
            database = cls.__database
            
            with cls.__app.app_context():
                if not cls.__newsletters:
                    query = Newsletter.query.all()
                    cls.__newsletters = [N for N in query]

                if not cls.__categories:
                    query = Category.query.all()
                    cls.__categories = [C for C in query]
        
        except Exception as error:
            print('DATABASE ERROR:', error)

        for post in list_of_posts:
            category = post.get('category')
            
            newsletter_list = list(filter(lambda x: x.name == name, cls.__newsletters))
            category_list = list(filter(lambda x: x.name == category, cls.__categories))    
            
            if newsletter_list == [] or category_list == []:
                print('ERROR: Newsletter or Category does not exist.')
            elif newsletter_list[0] and category_list[0]:
                with cls.__app.app_context():
                    title = post.get('title')
                    post_in_db = Post.query.filter_by(title=title).first()
                    if not post_in_db:
                        new_post = Post()
                        new_post.title = post.get('title')
                        new_post.description = post.get('description')
                        new_post.author = post.get('author')
                        new_post.url = post.get('url')
                        new_post.newsletter_id = newsletter_list[0].id
                        new_post.category_id = category_list[0].id
                        database.session.add(new_post)
                        database.session.commit()
                    else:
                        pass  # Post already in database
            else:
                pass  # There is no other case

    @classmethod
    def run_task(cls, app, database) -> None:
        """Run this method in a background task, this method execute the
        scrapers and send data in cls, this data is inserted in the database.

        Args
            app: An instance of Flask application.
            database: An instance of SQLAlchemy database.
        
        Returns:
            None - Run permanently.
        """
        cls.__database = database
        cls.__app = app

        while True:
            sleep(TIME_FOR_SLEEP)
            for newsletter in SCRAPER_LIST:
                # Execute subprocess
                print('######################################################')
                print(f"NEWSLETTER: {newsletter['name']}")
                print('######################################################')
                spider = BasicSpider(AutoScraperScraper())
                spider.execute_scraper(newsletter)
                result = spider.result()
                if result is not None:
                    cls.__insert_in_database(newsletter['name'], result)