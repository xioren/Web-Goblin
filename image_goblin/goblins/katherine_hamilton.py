from meta import MetaGoblin


class KatherineHamiltonGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'katherine hamilton goblin'
    ID = 'katherinehamilton'
    URL_PAT = r'https?://[^"\s\n]+\.jpg'
    MODIFIERS = ('', '-front', '-back', '-side', '-set', '-fton', '-open', '-fron-1')

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if '.jpg' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            url = self.parser.regex_sub(r'(-front|-back)?(-\d+x\d+)?\.jpg', '', url).strip('-')

            for mod in self.MODIFIERS:
                self.collect(f'{url}{mod}.jpg')

        self.loot()
