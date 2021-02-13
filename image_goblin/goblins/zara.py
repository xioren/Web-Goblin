from meta import MetaGoblin

# NOTE: used to use Inditex Group API

class ZaraGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'zara goblin'
    ID = 'zara'
    SIZE = 0
    # API_URL = 'https://www.zara.com/itxrest/1/catalog/store/11719/category/0/product/{}/detail' -> returns empty legacy response
    # URL_BASE = 'https://static.zara.net/photos'
    URL_PAT = r'https?://static[^"]+_\d+_\d+_\d+\.jpe?g'
    MODIFIERS = [f'_{j}_{k}_' for j in range(1, 7) for k in range(1, 21)]

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''remove scaling from query string'''
        return self.parser.regex_sub(r'&imwidth=\d+', '', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'static' in target:
                url_base, url_end = self.parser.regex_split(r'_\d+_\d+_\d+', target)

                for mod in self.MODIFIERS:
                    urls.append(f'{url_base}{mod}{self.SIZE}{self.trim(url_end)}')
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            self.collect(self.parser.regex_sub(r'w/\d+/', '', url))

        self.loot()
