from goblins.generic_iota import IotaGoblin


class FreePeopleGoblin(IotaGoblin):

    NAME = 'free people goblin'
    ID = 'freepeople'
    MODIFIERS = ('_a', '_b', '_c', '_d', '_e', '_vid')
    API_URL = 'https://www.freepeople.com/api/catalog/v0/fp-us/pools/US_DIRECT/products?slug={}&projection-slug=pdp'
    AUTH_API_URL = 'https://www.freepeople.com/slipstream/api/token/v0/fp-us/auth'

    def __init__(self, args):
        super().__init__(args)
