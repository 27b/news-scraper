from crawler.config import list_of_sites
from crawler.core.extractor import PostExtractor
from crawler.core.handler import PostHandler
from models import Newsletter, Category, Post
from time import sleep


TIME_FOR_SLEEP = 60 * 10
SCRAPER_LIST = list_of_sites


class CrawlerSchema:
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
            if self.check_database_status():
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
        self.schema = CrawlerSchema(app, db)
        self.newsletters = self.schema.get_newsletters()
        self.categories = self.schema.get_categories()
        self.newsletters_name = [N.name for N in self.newsletters]
        self.categories_name = [C.name for C in self.categories]

    def save_post(self, new_post: Post) -> bool:
        '''Save Post in database using CrawlerSchema if the post is valid.

        Args:
            Post: Post type.

        Returns:
            bool: True or false depending on the result of the database. 
        '''
        return self.schema.save_post_in_database(new_post)
        
    def check_if_post_is_valid(self, post: dict) -> Post | bool:
        '''Check if the newsltetter and category of the post is valid.
        
        Args:
            post: Is a dict with: title, description, author, url, category
                  and Newsletter.

        Returns:
            Post: if the post is valid.
            bool: False if category or newsletter is invalid.
        '''
        if not post.get('newsletter') in self.newsletters_name: return False
        if not post.get('category') in self.categories_name: return False

        newsletter = None
        category = None

        for n in self.newsletters:
            if n.name == post.get('newsletter'):
                newsletter = n
                
        for c in self.categories:
            if c.name == post.get('category'):
                category = c

        new_post = Post()
        new_post.title = post.get('title')
        new_post.description = post.get('description')
        new_post.author = post.get('author')
        new_post.url = post.get('url')
        new_post.newsletter_id = newsletter.id
        new_post.category_id = category.id

        return new_post


class Crawler:
    
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
                spider = PostHandler(PostExtractor())
                spider.execute_scraper(newsletter)
                result = spider.result()
                if result:
                    cls.send_data_to_handler(newsletter['name'], result)
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
