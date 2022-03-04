list_of_sites = [
    {
        'name': 'NYTimes',
        'categories': {
            'politics': [
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/politics'
                }
            ],
            'business': [
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/business'
                },
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/business/media'
                },
                {   
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/business/economy'
                },
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/business/energy-environment'
                },
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/business/small-business'
                },
            ],
            'technology': [
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/technology'
                },
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/technology/personaltech'
                },
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/spotlight/cybersecurity'
                },
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/topic/subject/social-media'
                }
            ],
            'science': [
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/science'
                }
            ],
            'world': [
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/world'
                }
            ],
            'books': [
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/books'
                }
            ],
            'automobile': [
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/automobiles'
                }
            ],
            'health': [
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/health'
                }
            ],
            'education': [
                {
                    'case': 'case-1',
                    'url': 'https://www.nytimes.com/section/education'
                }
            ],
            #'television': [
            #    {
            #        'case': 'case-1',
            #        'url': 'https://www.nytimes.com/section/movies'
            #    },
            #    #{
            #    #    'case': 'case-1',
            #    #    'url': 'https://www.nytimes.com/spotlight/what-to-watch'
            #    #}
            #],
            #'climate': [
            #    {
            #        'case': 'case-1',
            #        'url': 'https://www.nytimes.com/section/climate'
            #    }
            #]
        },
        'wanted_list': {
            'case-1': {
                'config_base_url': 'https://www.nytimes.com/',
                'container': 'div.css-13mho3u ol li',
                'title': 'li div div a h2::text',
                'description': 'li div div a p.css-1echdzn::text',
                'author': 'li div div a div.css-1nqbnmb.e140qd2t0 p',
                'url': 'li div div a::attr(href)'
            }
        }
    },
    {
        'name': 'Time',
        'categories': {
            'politics': [
                {
                    'case': 'case-1',
                    'url': 'https://time.com/section/politics/'
                }
            ],
            'business': [
                {
                    'case': 'case-1',
                    'url': 'https://time.com/section/business/'
                }
            ],
            'technology': [
                {
                    'case': 'case-1',
                    'url': 'https://time.com/section/tech/'
                }
            ],
            'science': [
                {
                    'case': 'case-1',
                    'url': 'https://time.com/section/science/'
                }
            ],
            'health': [
                {
                    'case': 'case-1',
                    'url': 'https://time.com/section/health/'
                }
            ],
            'climate': [
                {
                    'case': 'case-1',
                    'url': 'https://time.com/section/climate/'
                }
            ],
            'sports': [
                {
                    'case': 'case-1',
                    'url': 'https://time.com/section/sports/'
                }
            ],
            #'world': [
            #    {
            #        'case': 'case-1',
            #        'url': 'https://time.com/section/world/'
            #    }
            #]
        },
        'wanted_list': {
            'case-1': {
                'config_base_url': 'https://time.com/',
                'container': 'div.component.taxonomy-related-touts.section-related__touts div.taxonomy-tout',
                'title': 'div.text h2.headline::text',
                'description': 'h3.summary::text',
                'author': 'span.byline span:first-child::text',
                'url': 'div a::attr(href)'
            }
        }
    },
    {
        'name': 'WashingtonPost',
        'categories': {
            'politics': [
                {
                    'case': 'case-1',
                    'url': 'https://www.washingtonpost.com/politics/?itid=nb_politics'
                }
            ],
            'business': [
                {
                    'case': 'case-1',
                    'url': 'https://www.washingtonpost.com/economy/?itid=nb_business_economy'
                },
                {
                    'case': 'case-1',
                    'url': 'https://www.washingtonpost.com/economic-policy/?itid=nb_business_economic-policy'
                },
                #{
                #    'case': 'case-1',
                #    'url': 'https://www.washingtonpost.com/realestate/?itid=nb_business_real-estate'
                #}
            ],
            'technology': [
                {
                    'case': 'case-1',
                    'url': 'https://www.washingtonpost.com/business/technology/?itid=nb_technology'
                },
                {
                    'case': 'case-1',
                    'url': 'https://www.washingtonpost.com/technology/innovations/?itid=nb_technology_innovations'
                },
                {
                    'case': 'case-1',
                    'url': 'https://www.washingtonpost.com/tech-policy/?itid=nb_technology_tech-policy'
                }
            ],
        },
        'wanted_list': {
            'case-1': {
                'container': 'main article div ul.list-hide-bullets li.pb-md.b.bb.gray-darkest',
                'title': 'li.pb-md.b.bb.gray-darkest div.w-100.grid div.pr-xs a h3::text',
                'description': 'li.pb-md.b.bb.gray-darkest div.w-100.grid div.pr-xs p.pt-xs.pb-xs::text',
                'author': 'li.pb-md.b.bb.gray-darkest div.w-100.grid div.pr-xs span a::text',
                'url': 'li.pb-md.b.bb.gray-darkest div.w-100.grid div.pr-xs a::attr(href)'
            }
        }
    }
]
