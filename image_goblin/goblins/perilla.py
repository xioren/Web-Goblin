from meta import MetaGoblin

# TODO: add shoplo backend
# QUESTION: what happens when a single image is input?

class PerillaGoblin(MetaGoblin):
    '''accepts:
        - webpage
    '''

    NAME = 'perilla goblin'
    ID = 'perilla'
    URL_PAT = r'https?://cdn\.shoplo\.com/[^"\s]+'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            self.logger.log(2, self.NAME, 'looting', target)
            self.logger.spin()

            urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))
            self.delay()

        for url in urls:
            self.collect(self.parser.regex_sub(r'/th\d+/', '/orig/', url))

        self.loot()
