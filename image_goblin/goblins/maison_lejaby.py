from meta import MetaGoblin


class MaisonLejabyGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'maison lejaby goblin'
    ID = 'maisonlejaby'
    URL_PAT = r'maisonlejaby\.com/phototheque/[^"\s]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'phototheque' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            url_base = self.parser.regex_sub(r'[A-Z](\.[A-Z\d]+)?\.jpg', '', url).replace('medium', 'large')

            for mod in ('A', 'B', 'C', 'D', 'E', 'F'):
                self.collect(f'{url_base}{mod}.jpg')

        self.loot()
