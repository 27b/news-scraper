from crawler.config import list_of_sites
from crawler.core.scraper import AutoScraperScraper
from crawler.core.spider import BasicSpider
from models import Newsletter, Category, Post
from time import sleep
from sys import exit


TIME_FOR_SLEEP = 60 * 10
SCRAPER_LIST = list_of_sites


class CrawlerSchema:
    __instance = None

    def __init__(self, app, db):
        self.__app = app
        self.__db = db

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            instance = super().__call__(*args, **kwargs)
            cls.__instance = instance
        return cls.__instance

    def __check_database_status(self) -> bool:
        '''Checks if the database and the application were instantiated,
        it also checks if the newsletter exists in the database.'''
        if not self.__app:
            print('The application has not been instantiated.')
            return False
        
        if not self.__db:
            print('The database has not been instantiated.')
            return False
    
        return True

    def __get_categories(self) -> list[Category]:
        '''Returns a dictionary with all existing categories.'''
        with self.__app.app_context():
            query = Category.query.all() 
            return [C for C in query]

    def __get_newsletters(self) -> list[Newsletter]:
        '''Returns a dictionary with all existing newsletters'''
        with self.__app.app_context():
            query = Newsletter.query.all()
            return [N for N in query]

    def __save_post_in_database(self, new_post) -> bool:
        try:
            self.__db.session.add(new_post)
            self.__db.session.commit()
        except Exception as error:
            print(error)
            return False
        else:
            return True


class CrawlerMediator:
    '''Get data of crawler and apply logic to save data using crawler schema'''
    schema = CrawlerSchema()

    @classmethod
    def save_post(cls, new_post) -> bool:
        if cls.schema.__check_if_post_is_valid():
            return cls.schema.__save_post_in_database(new_post)
    
    @classmethod
    def check_if_post_is_valid(cls, new_post) -> bool:
        pass


class CrawlerManager:
    '''Execute Crawler and send data to mediator,'''
    
    @classmethod
    def execute_crawler():
        pass

    @classmethod
    def send_data_to_mediator():
        pass


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
            for newsletter in SCRAPER_LIST:
                # Execute subprocess
                print('------------------------------------------------------')
                print(f"NEWSLETTER: {newsletter['name']}")
                print('------------------------------------------------------')
                spider = BasicSpider(AutoScraperScraper())
                spider.execute_scraper(newsletter)
                result = spider.result()
                if result is not None:
                    cls.__insert_in_database(newsletter['name'], result)
            sleep(TIME_FOR_SLEEP)
