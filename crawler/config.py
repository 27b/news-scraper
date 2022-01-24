list_of_sites = [
    {
        'name': 'NYTimes',
        'categories': {
            'economy': [
                {   
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/business/economy'
                }
            ],
            'politics': [
                {
                    'case': 'case-2',
                    'url': 'https://www.nytimes.com/section/politics'
                }
            ],
            'technology': [
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/technology'
                }
            ]
        },
        'wanted_list': {
            'case-1': {
                'container': 'div.css-13mho3u ol',
                'title': 'li div div a h2::text',
                'description': 'li div div a p.css-1echdzn::text',
                'author': 'li div div a div.css-1nqbnmb.e140qd2t0 p',
                'url': ''
            }
        }
    }
]
