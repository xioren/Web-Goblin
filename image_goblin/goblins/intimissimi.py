from goblins.generic_gamma import GammaGoblin


class IntimissimiGoblin(GammaGoblin):

    NAME = 'intimissimi goblin'
    ID = 'intimissimi'
    MODIFIERS = ('FI', 'BI', 'M', 'DT1', 'C', 'B', 'F')
    IMG_PAT = r'(?<=/)\w+_wear\w+_\w{2}\.jpg'
    ITER_PAT = r'\w{2}(?=\.)'
    URL_BASE = 'https://www.intimissimi.com/dw/image/v2/BCXQ_PRD/on/demandware.static/-/Sites-INT_EC_COM/default/images/'
    QUERY = '?sw=3000&sfrm=jpeg&q=100'

    def __init__(self, args):
        super().__init__(args)
