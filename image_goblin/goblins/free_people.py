from goblins.generic_iota import IotaGoblin


class FreePeopleGoblin(IotaGoblin):

    NAME = 'free people goblin'
    ID = 'freepeople'
    MODIFIERS = ('a', 'b', 'c', 'd', 'e', 'vid')
    API_URL = 'https://www.freepeople.com/api/catalog/v0/fp-{}/pools/{}_DIRECT/products?slug={}&projection-slug=pdp'
    AUTH_API_URL = 'https://www.freepeople.com/slipstream/api/token/v0/fp-us/auth'
    BACKUP_URLS = {'fp-uk': 'https://images.freepeople.com/is/image/FreePeople',
                   'fp-de': 'https://images.freepeople.com/is/image/FreePeople',
                   'fp-fr': 'https://images.freepeople.com/is/image/FreePeople',
                   "fp-us": 'https://images.freepeople.com/is/image/FreePeople',
                   "fp-ca": 'https://images.freepeople.com/is/image/FreePeople'}

    def __init__(self, args):
        super().__init__(args)

    def is_alt(self, url):
        return False

    def localize_api_url(self, site_id, slug):
        country = site_id.split('-')[1]
        region = {'uk': "INTL", "us": "US", "ca": "CA", "de": "INTL", "fr": "INTL"}
        return self.API_URL.format(country, region[country], slug)
