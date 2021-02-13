from meta import MetaGoblin


class MGMGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'mgm models goblin'
    ID = 'mgm'
    API_URL = 'https://www.mgm-models.de/api'
    CDN_URL = 'https://strg.global'
    SIZE = '1920'

    def __init__(self, args):
        super().__init__(args)

    def extract_model(self, url):
        '''extract model name from url'''
        return url.rstrip('/').split('/')[-1]

    def extract_images(self, images):
        '''extract images from json object'''
        return [f'{self.CDN_URL}/{image.get("url", "")}' for image in images]

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'strg.global' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                model = self.extract_model(target)
                response = self.parser.load_json(self.get(f'{self.API_URL}/models/{model}').content)

                for section in ('images', 'polaroids', 'setcardImages'):
                    urls.extend(self.extract_images(response.get(section, {})))

                # for video in response.get('videos', ''):
                #     self.logger.log(1, self.NAME, 'video url', f'https://player.vimeo.com/video/{video["url"]}')

            self.delay()

        for url in urls:
            self.collect(url.replace('%SIZE%', self.SIZE))

        self.loot()
