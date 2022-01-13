from autoscraper import AutoScraper
from time import sleep


scraper = AutoScraper()

url = 'https://www.nytimes.com/section/business/economy'


if __name__ == '__main__':
    first_message = input('You can load "nytimes-memory"? Y/n: ')
    if first_message == 'y' or first_message == 'Y':
        scraper.load('memory/nytimes-economy')
        result = scraper.build(url)
        sleep(1)
        for r in result:
            print(f'USING MEMORY: {r}')
    else:
        wanted_list = [
            "Inflation is too high, President Biden’s pick for Fed vice chair says as her nomination hearing begins.",
            "Lael Brainard, the Federal Reserve governor who President Biden nominated for vice chair, said the central bank is focused on getting price gains back down.",
            "Jeanna Smialek"
        ]
        result = scraper.build(url, wanted_list)
        sleep(1)
        for r in result:
            print(f'NOT USING MEMORY: {r}')

    second_message = input('You can save the model? Y/n: ')
    if second_message == 'y' or second_message == 'Y':
        scraper.save('memory/nytimes-economy')
