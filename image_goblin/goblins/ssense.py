from meta import MetaGoblin


class SsenseGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'ssense goblin'
    ID = 'ssense'
    URL_PAT = r'https?://(img\.ssensemedia|res\.cloudinary)\.com/(images?|ssenseweb)/[^"\s]+'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return self.parser.regex_search(r'[A-Z\d]+(?=_\d)', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'img.ssensemedia' in target or 'res.cloudinary' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            id = self.extract_id(url)

            for n in range(6):
                self.collect(f'https://img.ssensemedia.com/images/{id}_{n}/{id}_{n}.jpg')

        self.loot()
