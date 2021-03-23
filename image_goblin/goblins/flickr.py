from meta import MetaGoblin


class FlickrGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'flickr goblin'
    ID = 'flickr'
    API_URL = 'https://api.flickr.com/services/rest?extras=url_o&photo_id={}&method=flickr.photos.getInfo&csrf=&api_key=28113eec9eec551a14495a6659dec19d&format=json&hermes=1&hermesClient=1&nojsoncallback=1'
    # URL_PAT = r'live\.staticflickr\.com[\\/\d]+_[a-z\d]+_o\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return self.parser.regex_search(r'(?<=photos/)\w+/\d+', url).split('/')[1]

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if '.static' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                image_id = self.extract_id(target)
                response = self.parser.load_json(self.get(self.API_URL.format(image_id)).content)

                if 'photo' in response:
                    urls.append(response['photo']['url_o'])

            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
