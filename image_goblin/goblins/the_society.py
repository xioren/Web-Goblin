from meta import MetaGoblin


class TheSocietyGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'the society goblin'
    ID = 'thesociety'
    API_URL = 'https://www.thesocietymanagement.com/api'

    def __init__(self, args):
        super().__init__(args)

    def extract_info(self, url):
        '''extract model division and id'''
        return self.parser.regex_search(r'[a-z]+/\d+(?=-)', url).split('/')

    def extract_images(self, images, key='src_hd'):
        '''extract images from json object'''
        return [image[key] for image in images]

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'media.thesocietymanagement' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target.replace('.jpg', '_M.JPG'))
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                division, id = self.extract_info(target)
                response = self.parser.from_json(self.get(f'{self.API_URL}/models/{division}/{id}').content)

                for section in ('portfolio', 'pola'):
                    urls.extend(self.extract_images(response['books'][section]))

                if 'video' in response['books']:
                    urls.extend(self.extract_images(response['books']['video'], key='video'))

            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
