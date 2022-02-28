from unicodedata import category
from crawler.config import list_of_sites
from crawler.core.scraper import AutoScraperScraper
from crawler.core.spider import BasicSpider
from models import Newsletter, Category, Post
from time import sleep
from sys import exit


TIME_FOR_SLEEP = 60 * 10
SCRAPER_LIST = list_of_sites


class __CrawlerSchema:
    '''CrawlerSchema is the handler of the database.
    
    Args:
        app: An instance of Flask application.
        database: An instance of SQLAlchemy database.
    '''
    __instance = None

    def __init__(self, app, db):
        self.__app = app
        self.__db = db

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            instance = super().__call__(*args, **kwargs)
            cls.__instance = instance
        return cls.__instance

    def check_database_status(self) -> bool:
        '''Checks if the database and the application were instantiated,
        it also checks if the newsletter exists in the database.'''
        if not self.__app:
            print('The application has not been instantiated.')
            return False

        if not self.__db:
            print('The database has not been instantiated.')
            return False

        return True

    def get_categories(self) -> list[Category]:
        '''Returns a dictionary with all existing categories.'''
        with self.__app.app_context():
            query = Category.query.all() 
            return [C for C in query]

    def get_newsletters(self) -> list[Newsletter]:
        '''Returns a dictionary with all existing newsletters.'''
        with self.__app.app_context():
            query = Newsletter.query.all()
            return [N for N in query]

    def save_post_in_database(self, new_post: Post) -> bool:
        '''Save post in database using app context.
        
        Args:
            new_post: Post type.

        Returns:
            True: If the post was saved in the database.
            False: If an error occurred.
        '''
        try:
            if self.__check_database_status():
                with self.__app.app_context():
                    self.__db.session.add(new_post)
                    self.__db.session.commit()
            else:
                return False

        except Exception as error:
            print('SAVE POST ERROR:', error)
            return False
        else:
            return True


class CrawlerDataHandler:
    '''Get data of crawler and apply logic to save data using crawler schema.
    
    Args:
        app: An instance of Flask application.
        database: An instance of SQLAlchemy database.
    '''

    def __init__(self, app, db) -> None:
        self.schema = __CrawlerSchema(app, db)
        self.newsletters = [N.name for N in self.schema.get_newsletters()]
        self.categories = [C.name for C in self.schema.get_categories()]

    def save_post(cls, new_post: Post) -> bool | None:
        '''Save Post in database using CrawlerSchema if the post is valid.

        Args:
            Post: Post type.

        Returns:
            bool: True or false depending on the result of the database. 
        '''
        if cls.schema.__check_if_post_is_valid(new_post):
            return cls.schema.__save_post_in_database(new_post)
    
    def check_if_post_is_valid(self, post: dict) -> Post | bool:
        '''Check if the newsltetter and category of the post is valid.
        
        Args:
            post: Is a dict with: title, description, author, url, category
                  and Newsletter.

        Returns:
            Post: if the post is valid.
            bool: False if category or newsletter is invalid.
        '''
        if not post.category in self.categories: return False
        if not post.newsletter in self.newsletters: return False
        
        # Next: Change database query for lambda
        newsletter_query = Newsletter.query.filter_by(name=post.newsletter)
        category_query = Category.query.filter_by(name=post.category)
        
        new_post = Post()
        new_post.title = post.get('title')
        new_post.description = post.get('description')
        new_post.author = post.get('author')
        new_post.url = post.get('url')
        new_post.newsletter_id = newsletter_query.first()
        new_post.category_id = category_query.first()

        return new_post


class Crawler2:
    
    @classmethod
    def run_task(cls, app, db) -> None:
        '''This method execute the scrapers and send data in cls, this data
        is inserted in the database.

        Args:
            app: An instance of Flask application.
            db: An instance of SQLAlchemy database.
        
        Returns:
            None - Run permanently.
        '''
        cls.__app = app
        cls.__db = db

        while True:
            for newsletter in SCRAPER_LIST:
                print(f"* NEWSLETTER: {newsletter['name']}")
                spider = BasicSpider(AutoScraperScraper())
                spider.execute_scraper(newsletter)
                result = spider.result()
                if result: cls.send_data_to_handler(newsletter['name'], result)
            sleep(TIME_FOR_SLEEP)

    @classmethod
    def send_data_to_handler(cls, newsletter: str, post_list: list[dict]):
        '''Send data to Data Handler and check if the post is valid, if is
        valid save the data.
        
        Args:
            newsletter: The name in lowercase of the newsletter.
            post_list: A list of dictionaries with the attributes of Post.
        
        Returns:
            None: You can extend this if you want add logs of the state of
            posts.
        '''
        data_handler = CrawlerDataHandler(cls.__app, cls.__db)
        for post in post_list:
            post['newsletter'] = newsletter
            new_post = data_handler.check_if_post_is_valid(post)
            if new_post:
                data_handler.save_post(new_post)


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
