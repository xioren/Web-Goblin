from goblins.generic_gamma import GammaGoblin


class PrincesseTamTamGoblin(GammaGoblin):

    NAME = 'princesse tamtam goblin'
    ID = 'princessetamtam'
    MODIFIERS = ['PA']
    IMG_PAT = r'[A-Z\d]+_\d+_[A-Z\d]+\.jpg'
    ITER_PAT = r'(?<=_)[A-Z\d]+(?=\.)'
    URL_BASE = 'https://www.princessetamtam.com/dw/image/v2/ABBK_PRD/on/demandware.static/-/Sites-ptt-master/default/'
    QUERY = '?q=100'

    def __init__(self, args):
        super().__init__(args)
        for char in ('PF', 'OP'):
            for n in range(1, 5):
                self.MODIFIERS.append(f'{char}{n}')
