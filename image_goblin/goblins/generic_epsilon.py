from meta import MetaGoblin

# NOTE: may work for trendyol and penti

class EpsilonGoblin(MetaGoblin):
    '''handles: Medianova CDN
    docs: https://docs.medianova.com/image-resize-and-optimization-module/
    accepts:
        - image
        - webpage
    generic back-end for:
        - koton
        - lc waikiki
        - yargici
    '''

    NAME = 'epsilon goblin'
    ID = 'epsilon'

    def __init__(self, args):
        super().__init__(args)

    def trim_url(self, url):
        '''remove scaling from url'''
        return self.parser.regex_sub(r'mnresize/\d+/(\d+|-)//?', '', url).replace('Thumbs', 'Originals')

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'mncdn' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            url_base, _ = self.parser.regex_split(self.MOD_PAT, self.trim_url(url))

            self.generate_modifiers(url)
            for mod in self.modifiers:
                self.collect(f'{url_base}{mod}{self.URL_END}')

        self.loot()
