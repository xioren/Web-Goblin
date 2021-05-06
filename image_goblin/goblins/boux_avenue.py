from goblins.generic_gamma import GammaGoblin

# NOTE: can work with web too but url needs query string

class BouxAvenueGoblin(GammaGoblin):

    NAME = 'boux avenue goblin'
    ID = 'bouxavenue'
    MODIFIERS = ('FR', 'BK', 'ST')
    IMG_PAT = r'(?<=/)[\d+_[A-Z\d]+_\d_[A-Z\d]+\.jpg'
    ITER_PAT = r'[A-Z\d]+(?=\.)'
    URL_BASE = 'https://www.bouxavenue.com/on/demandware.static/-/Sites-bouxavenue-master-catalog/default/'
    QUERY = ''

    def __init__(self, args):
        super().__init__(args)
