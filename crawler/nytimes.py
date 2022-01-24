import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime as dt
from re import compile


process = CrawlerProcess()


class NYTimesScraper(scrapy.Spider):
    name = 'NYTimes-Scraper'
    start_urls = [
        'https://www.nytimes.com/section/business/economy'
    ]

    def parse(response):
        post = response.css('div.css-13mho3u ol')
        title = post.css('li div div a h2::text').getall()
        description = post.css('li div div a p.css-1echdzn::text').getall()
        author = post.css('li div div a div.css-1nqbnmb.e140qd2t0 p').getall()
        return [
            {
                'title': post[0],
                'description': post[1],
                'author': compile(r'<[^>]+>').sub('', post[2]).split('By ')[1],
                'datetime': dt.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }
            for post in list(zip(title, description, author))
        ]


if __name__ == '__main__':
    process.crawl(NYTimesScraper)
    process.start()