from meta import MetaGoblin

# TODO: add bigcommerce cdn generic goblin

class AmericanApparelGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'american apparel goblin'
    ID = 'americanapparel'
    URL_PAT = r'https?://cdn\d+\.bigcommerce\.com/[^/]+/images/stencil/[^/]+' \
              r'/products/\d+/\d+/[a-z\d]+_[a-z\d]+_[^"\s]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'bigcommerce' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(self.parser.dequery(target))
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            self.collect(self.parser.regex_sub(r'(?<=stencil/)[^/]+', 'original', url))

        self.loot()
