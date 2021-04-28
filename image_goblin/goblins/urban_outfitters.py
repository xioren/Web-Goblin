from goblins.generic_iota import IotaGoblin


class UrbanOutfittersGoblin(IotaGoblin):

    NAME = 'urban outfitters goblin'
    ID = 'urbanoutfitters'
    MODIFIERS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '0', 'vid')
    API_URL = 'https://www.urbanoutfitters.com/api/catalog/v0/uo-{}/pools/{}_DIRECT/products?slug={}&projection-slug=pdp'
    AUTH_API_URL = 'https://www.urbanoutfitters.com/slipstream/api/token/v0/uo-us/auth'
    ALT_API_URL = 'urbanoutfitters.com/api/product/s'
    BACKUP_URLS = {'uo-uk': 'https://euimages.urbanoutfitters.com/is/image/UrbanOutfittersEU',
                   'uo-de': 'https://euimages.urbanoutfitters.com/is/image/UrbanOutfittersEU',
                   'uo-fr': 'https://euimages.urbanoutfitters.com/is/image/UrbanOutfittersEU',
                   "uo-us": 'https://images.urbanoutfitters.com/is/image/UrbanOutfitters',
                   "uo-ca": 'https://images.urbanoutfitters.com/is/image/UrbanOutfitters'}

    def __init__(self, args):
        super().__init__(args)

    def is_alt_api(self, url):
        for loc in ['au.urbanoutfitters', 'hk.urbanoutfitters', 'sg.urbanoutfitters']:
            if loc in url:
                return True
        return False

    def localize_api_url(self, site_id, slug):
        country = site_id.split('-')[1]
        region = {'uk': "INTL", "us": "US", "ca": "CA", "de": "INTL", "fr": "INTL"}
        return self.API_URL.format(country, region[country], slug)
