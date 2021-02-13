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

    def split_url(self, url):
        '''split url into base, end and sub out scalinging'''
        return self.parser.regex_split(r'_(0\d)?(?=_)', self.parser.regex_sub(r'(?<=stencil/)[^/]+', 'original', url), maxsplit=1)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'bigcommerce' in target:
                urls.append(self.parser.dequery(target))
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            url_base, _, url_end = self.split_url(url)
            for mod in ('', '01', '02', '03', '04'):
                self.collect(f'{url_base}_{mod}{url_end}')

        self.loot()
