from meta import MetaGoblin


class GuessGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'guess goblin'
    ID = 'guess'
    URL_PAT = r'https?://[^"\s\']+/image/upload/[^"\s\']+/Style/[^"\s\'\)]+'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''scale and return url base'''
        return self.parser.regex_sub(r'(?<=upload/).+/v1/|-ALT\d', '', self.parser.dequery(url))

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'image/upload' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            url_base = self.trim(self.parser.sanitize(url))

            for id in ('', '-ALT1', '-ALT2', '-ALT3', '-ALT4'):
                self.collect(f'{url_base}{id}')

        self.loot()
