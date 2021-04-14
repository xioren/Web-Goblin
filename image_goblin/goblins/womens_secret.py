from goblins.generic_gamma import GammaGoblin


# NOTE: https://womensecret.com/on/demandware.store/Sites-WS-Site/es_ES/GTM-GetProductJSON?pid=
# NOTE: https://womensecret.com/on/demandware.store/Sites-WS-Site/es_ES/GTM-GetProductJSON?pid=4989295

class WomensSecretGoblin(GammaGoblin):

    NAME = 'womens secret goblin'
    ID = 'womensecret'
    MODIFIERS = ('FM', 'TM', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8')
    IMG_PAT = r'P_[A-Z\d]+\.jpg'
    ITER_PAT = r'[A-Z\d]{2}(?=\.)'
    URL_BASE = 'https://womensecret.com/on/demandware.static/-/Sites-gc-ws-master-catalog/default/images/hi-res/'
    QUERY = ''

    def __init__(self, args):
        super().__init__(args)
