from meta import MetaGoblin


class ShopbopGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'shopbop goblin'
    ID = 'shopbop'
    URL_PAT = r'https?://[a-z\-\.]+amazon\.com[^"\s]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def prep(self, url):
        '''prepare the url by removing scaling and mobile elements'''
        return self.parser.regex_sub(r'._\w+(_\w+)?_\w+_', '', url).replace('m.media', 'images-na.ssl-images').replace('2-1', '2-0')

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'amazon' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            url = self.prep(url)

            for n in range(1, 7):
                self.collect(self.parser.regex_sub(r'q\d', f'q{n}', url))

        self.loot()
