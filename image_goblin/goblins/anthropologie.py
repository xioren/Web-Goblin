from goblins.generic_iota import IotaGoblin


# BUG: international api is broken and returns items ids that dont exists.


class AnthropologieGoblin(IotaGoblin):

    NAME = 'anthropologie goblin'
    ID = 'anthropologie'
    MODIFIERS = [f'{m}{n}' if n > 1 else f'{m}' for n in range(1, 6) for m in ('b', 'c')]
    API_URL = 'https://www.anthropologie.com/api/catalog/v0/an-{}/pools/{}_DIRECT/products?slug={}&projection-slug=pdp'
    AUTH_API_URL = 'https://www.anthropologie.com/slipstream/api/token/v0/an-us/auth'
    URL = 'https://s7d5.scene7.com/is/image/Anthropologie'
    BACKUP_URLS = {'an-uk': 'https://images.anthropologie.com/is/image/Anthropologie',
                   'an-de': 'https://images.anthropologie.com/is/image/Anthropologie',
                   'an-fr': 'https://images.anthropologie.com/is/image/Anthropologie',
                   "an-us": 'https://images.anthropologie.com/is/image/Anthropologie',
                   "an-ca": 'https://images.anthropologie.com/is/image/Anthropologie'}

    def __init__(self, args):
        super().__init__(args)

    def is_alt(self, url):
        return False

    def localize_api_url(self, site_id, slug):
        country = site_id.split('-')[1]
        region = {'uk': "INTL", "us": "US", "ca": "CA", "de": "INTL", "fr": "INTL"}
        return self.API_URL.format(country, region[country], slug)
