from meta import MetaGoblin


# NOTE: used to use Magento API


class AgentProvocateurGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'agent provocateur goblin'
    ID = 'agentprovocateur'
    BASE_URL = 'https://www.agentprovocateur.com'
    API_URL = BASE_URL + '{}/api/n/bundle'

    def __init__(self, args):
        super().__init__(args)

    def extract_path(self, url):
        '''return relative url path'''
        return self.parser.dequery(url).split('#')[0].split('/')[-1]

    def isolate(self, url):
        '''isolate original url from processed url'''
        if 'tco-images' in url:
            return url.split(')/')[-1]
        return url

    def extract_location(self, url):
        '''extract location from url'''
        return self.parser.regex_search(r'/[a-z]+_[a-z]+', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'media/catalog' in target:
                base = self.isolate(target).split('_')[0]
                zero = self.parser.regex_search(r'0(?=\d\.jpg)', target)

                for n in range(1, 6):
                    urls.append(f'{base}_ecom_{zero}{n}.jpg')
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                location = self.extract_location(target)
                self.headers.update({'Content-Type': 'application/json'})
                POST_DATA = self.parser.make_json({"requests":[{"action":"route",
                                                                "children":[{"path":f"/{self.extract_path(target)}",
                                                                             "_reqId":0}]}]})
                response = self.parser.load_json(self.post(self.API_URL.format(location), data=POST_DATA).content)

                for entry in response.get('catalog', ''):
                    for image in entry.get('media', ''):
                        urls.append(f'{self.BASE_URL}/static/media/catalog{image["image"]}')

            self.delay()

        for url in urls:
            if 'flatshot' not in url: # skip product images
                self.collect(url)

        self.loot()
