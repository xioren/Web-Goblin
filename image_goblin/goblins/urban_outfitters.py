from goblins.generic_iota import IotaGoblin


class UrbanOutfittersGoblin(IotaGoblin):

    NAME = 'urban outfitters goblin'
    ID = 'urbanoutfitters'
    MODIFIERS = ('_a', '_b', '_c', '_d', '_e', '_f', '_g', '_h', '_0', '_vid')
    API_URL = 'https://www.urbanoutfitters.com/api/catalog/v0/uo-us/pools/US_DIRECT/products?slug={}&projection-slug=pdp'
    AUTH_API_URL = 'https://www.urbanoutfitters.com/slipstream/api/token/v0/uo-us/auth'

    def __init__(self, args):
        super().__init__(args)
