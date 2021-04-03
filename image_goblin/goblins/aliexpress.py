from meta import MetaGoblin


class AliExpressGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'aliexpress goblin'
    ID = 'aliexpress'

    def __init__(self, args):
        super().__init__(args)
        self.MEDIA_URL = self.parser.regex_pattern('https?://ae0\d+\.alicdn\.com/[a-z\d]+/\w+/[^"\s]+')

    def extract_hash(self, url):
        '''extract unique hash'''
        return self.parser.regex_search(r'(?<=/[a-z\d]{2}/)\w+(?=/)', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if '.alicdn.' in target:
                urls.append(target)
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(self.parser.dequery(target)).content, self.MEDIA_URL))

            self.delay()

        for url in urls:
            self.collect(self.parser.regex_sub(r'_\d+x\d+\.jpg(_\.[a-z]+)?', '', url), filename=self.extract_hash(url))

        self.loot()
