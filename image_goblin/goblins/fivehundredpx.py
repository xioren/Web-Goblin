from meta import MetaGoblin


class FiveHundredpxGoblin(MetaGoblin):
    '''
    accepts:
        - image
        - webpage
    '''

    NAME = '500px goblin'
    ID = '500px'
    PHOTO_URL = 'https://api.500px.com/v1/photos?ids={}&image_size%5B%5D=2048'
    # QUESTION: do these hashes rotate?
    PROFILE_URL = 'https://api.500px.com/graphql?operationName=ProfileRendererQuery&variables=%7B%22username%22%3A%22{}%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22fcecc7028c308115b0defebc63acec3fe3c12df86a602c3e1785ba5cfb8fff47%22%7D%7D'
    PROFILE_PHOTOS_URL = 'https://api.500px.com/graphql?operationName=OtherPhotosQuery&variables=%7B%22username%22%3A%22{}%22%2C%22pageSize%22%3A{}%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22018a5e5117bd72bdf28066aad02c4f2d8acdf7f6127215d231da60e24080eb1b%22%7D%7D'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id'''
        return self.parser.regex_search(r'(?<=photo/)\d+', url)

    def extract_username(self, url):
        return self.parser.regex_search(r'(?<=/p/)\w+', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:
            self.logger.log(2, self.NAME, 'looting', target)
            self.logger.spin()

            if '/photo/' in target:
                # NOTE: download single post/image
                id = self.extract_id(target)
                response = self.parser.from_json(self.get(self.PHOTO_URL.format(id)).content)
                self.collect(response['photos'][id].get('image_url', '')[0], filename=id)
            else:
                # NOTE: download all profile images
                username = self.extract_username(target)
                response = self.parser.from_json(self.get(self.PROFILE_URL.format(username)).content)
                num_photos = response['data']['profile']['photos'].get('totalCount', 0)
                if num_photos == 0:
                    continue
                ids = []
                response = self.parser.from_json(self.get(self.PROFILE_PHOTOS_URL.format(username, num_photos)).content)
                for edge in response['data']['user']['photos']['edges']:
                    ids.append(edge['node'].get('legacyId', ''))
                # NOTE: can only request maximum 100 at a time
                for group in [ids[i:i + 100] for i in range(0, len(ids), 100)]:
                    response = self.parser.from_json(self.get(self.PHOTO_URL.format(','.join(group))).content)
                    for id in response.get('photos', ''):
                        self.collect(response['photos'][id].get('image_url', '')[0], filename=id)

            self.delay()

        self.loot()
