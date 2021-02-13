from meta import MetaGoblin


class GettyGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'getty goblin'
    ID = 'getty'
    URL_PAT = r'https?://[^"]+id\d+'

    def __init__(self, args):
        super().__init__(args)

    def upgrade(self, image):
        '''sub in higher resolution scaling'''
        id = self.parser.regex_search(r'id\d+', image)
        return f'https://media.gettyimages.com/photos/picture-{id}?s=2048x2048'

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'media' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            self.collect(self.upgrade(url))

        self.loot()
