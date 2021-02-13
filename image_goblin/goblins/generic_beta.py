from meta import MetaGoblin


# NOTE: fmt=png works as well


class BetaGoblin(MetaGoblin):
    '''handles: Adobe Dynamic Media Image Serving and Image Rendering API (scene7)
    docs: https://docs.adobe.com/content/help/en/dynamic-media-developer-resources/image-serving-api/image-serving-api/http-protocol-reference/command-reference/c-command-reference.html
    accepts:
        - image
        - webpage
    generic backend for:
        - calvin klein
        - esprit
        - hot topic
        - tommy hilfiger
    '''

    NAME = 'beta goblin'
    ID = 'beta'
    URL_PAT = fr'https?://[a-z\d\-]+\.scene7\.com/is/image/[A-Za-z]+/\w+(_\w+)?_\w+'
    QUERY = '?fmt=jpeg&qlt=100&scl=1'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return self.parser.regex_search(r'\w+(_\w+)?(?=_\w+)', url)

    def extract_base(self, url):
        '''extract url base'''
        return self.parser.regex_sub(r'(?<=/)[^/]+$', '', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'scene7' in target:
                urls.append(self.parser.dequery(target))
            else:
                if self.ACCEPT_WEBPAGE:
                    self.logger.log(2, self.NAME, 'looting', target)
                    self.logger.spin()
                    
                    urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))
                else:
                    self.logger.log(2, self.NAME, 'WARNING', 'webpage urls not supported', once=True)

            self.delay()

        for url in urls:
            id = self.extract_id(url)
            self.url_base = self.extract_base(url)

            for mod in self.MODIFIERS:
                self.collect(f'{self.url_base}{id}{mod}{self.QUERY}')

        self.loot()
