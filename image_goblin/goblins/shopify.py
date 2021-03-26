from goblins.generic_theta import ThetaGoblin


# NOTE: front end for use with --goblin cammand line argument


class ShopifyGoblin(ThetaGoblin):

    NAME = 'shopify goblin'
    ID = 'shopify'

    def __init__(self, args):
        super().__init__(args)
