from autoscraper import AutoScraper
from time import sleep


scraper = AutoScraper()
url = 'https://www.nytimes.com/section/business/economy'


if __name__ == '__main__':
    wanted_dict = {
        'title': ["Inflation is too high, President Biden’s pick for Fed vice chair says as her nomination hearing begins."],
        'description': ["Lael Brainard, the Federal Reserve governor who President Biden nominated for vice chair, said the central bank is focused on getting price gains back down."],
        'author': ["Jeanna Smialek"]
    }
    # Run scraper
    scraper.build(url, wanted_dict=wanted_dict)

    # group and organize results
    r = scraper.get_result_similar(
        url, keep_order=True, grouped=True, group_by_alias=True
    )

    # Separate results
    r_zip = list(zip(r['title'], r['description'], r['author']))

    items = [
        {'title': i[0], 'description': i[1], 'author': i[2]} for i in r_zip
    ]

    print(items)
