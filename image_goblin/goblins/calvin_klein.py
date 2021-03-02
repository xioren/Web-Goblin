from goblins.generic_beta import BetaGoblin


class CalvinKleinGoblin(BetaGoblin):

    NAME = 'calvin klein goblin'
    ID = 'calvinklein'
    ACCEPT_WEBPAGE = True
    QUERY = '?fmt=jpeg&qlt=100&scl=1.1'
    MODIFIERS = [f'_alternate{n}' if n > 0 else '_main' for n in range(5)]

    def __init__(self, args):
        super().__init__(args)
