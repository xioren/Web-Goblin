from meta import MetaGoblin


class AdoreMeGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'adore me goblin'
    ID = 'adoreme'
    API_URL = 'https://www.adoreme.com/v7/catalog/products/permalink'

    def __init__(self, args):
        super().__init__(args)

    def extract_slug(self, url):
        '''extract slug from url'''
        return self.parser.dequery(url).rstrip('/').split('/')[-1]

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'media-resize' in target:
                urls.append(target)
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                slug = self.extract_slug(target)
                response = self.parser.from_json(self.get(f'{self.API_URL}/{slug}').content)

                # NOTE: other colors are located in related products

                for image in response.get('gallery', ''):
                    urls.append(image['url'])

            self.delay()

        for url in urls:
            self.collect(self.parser.regex_sub(r'(?<=resize/)[^/]+', '0', url), filename=self.parser.regex_search(r'[^/]+(?=/full)', url))

        self.loot()
