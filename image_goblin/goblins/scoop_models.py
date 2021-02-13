from meta import MetaGoblin

class ScoopGoblin(MetaGoblin):
    '''accepts:
        - webpage
    '''

    NAME = 'scoop models goblin'
    ID = 'scoop'
    API_URL = 'https://scoopmodels.com/api/get_model'
    MEDIA_URL = 'https://scoopmodels.com/uploads/media'

    def __init__(self, args):
        super().__init__(args)

    def extract_slug(self, url):
        '''extract model slug from url'''
        return self.parser.regex_search(r'(?<=model/)[^/]+', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'uploads/media' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(self.parser.regex_sub(r'\d+x\d+', 'original', target))
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                slug = self.extract_slug(target)

                response = self.parser.load_json(self.post(self.API_URL, data={'slug': slug}).content)

                # NOTE: filename present but different than url media id
                # NOTE: video book present in json but not used

                if 'data' in response:
                    for book in response['data']['model']['books']:
                        for item in response['data']['model']['books'][book]:
                            for piece in item['pieces']:
                                if piece == None:
                                    continue
                                urls.append(f'{self.MEDIA_URL}/{piece["media_id"]}_original.{piece["metadata"]["media"]["file_ext"]}')

            self.delay()


        for url in urls:
            self.collect(url)

        self.loot()
