from meta import MetaGoblin


class EtaGoblin(MetaGoblin):
    '''handles: adis.ws
    accepts:
        - image
        - webpage
    generic back-end for:
        - boohoo
        - nasty gal
    '''

    NAME = 'eta goblin'
    ID = 'eta'
    QUERY = '?scl=1&qlt=100'
    URL_PAT = 'https?://i\d\.adis\.ws/i/boohooamplience/[^/]+/[^"]+'
    URL_BASE = 'https://i1.adis.ws/i/boohooamplience'
    MODIFIERS = [f'_{n}' for n in range(1, 10)]

    def __init__(self, args):
        super().__init__(args)
        self.MODIFIERS.insert(0, '')

    def get_sku(self, url):
        '''trim the url down'''
        return self.parser.regex_search(r'[a-z\d]+_[a-z\d]+_[a-z\d]+', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if '/i/' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            for mod in self.MODIFIERS:
                self.collect(f'{self.URL_BASE}/{self.get_sku(url)}{mod}.jpg{self.QUERY}')

        self.loot()
