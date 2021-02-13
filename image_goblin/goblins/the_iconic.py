from meta import MetaGoblin


class TheIconicGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'the iconic goblin'
    ID = 'theiconic'
    URL_PAT = r'(\d+-){2}\d\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return self.parser.regex_search(r'\d+-\d+-', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'img1' in target or 'static' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            id = self.extract_id(url)

            for n in range(1, 6):
                self.collect(f'https://static.theiconic.com.au/p/{id}{n}.jpg')

        self.loot()
