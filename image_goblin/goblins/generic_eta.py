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
    URL_PAT = r'media.[a-z]+.com/i/[a-z]+/[\w_]+'
    MODIFIERS = [f'_{n}' for n in range(1, 10)]

    def __init__(self, args):
        super().__init__(args)
        self.MODIFIERS.insert(0, '')

    def __str__(self):
        return 'eta goblin'

    def __repr__(self):
        return 'eta'

    def trim(self, url):
        '''trim the url down'''
        return self.parser.regex_search(self.URL_PAT, url).rstrip("_s/")

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
                self.collect(f'{self.trim(url)}{mod}.jpg{self.QUERY}')

        self.loot()
