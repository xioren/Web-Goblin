from meta import MetaGoblin


class NellyGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'nelly goblin'
    ID = 'nelly'
    QUERY = '?qlt=100'
    URL_BASE = 'https://i8.amplience.net/i/nlyscandinavia'
    URL_BASE_ALT = 'https://media.nelly.com/i/nlyscandinavia'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        if 'nlyscandinavia' in url: # image
            return self.parser.dequery(url).strip('/').split('/')[-2][:-3]
        else: # webpage
            return '-'.join(url.strip('/').split('-')[-2:])

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:

            id = self.extract_id(target)

            for n in range(1, 6):
                self.collect(f'{self.URL_BASE}/{id}_0{n}{self.QUERY}')

            if '/i/' not in target:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                response = self.get(target).content
                video_url = self.parser.regex_search(r'https://[^"]+/mp4_product_high', response)
                if video_url:
                    self.collect(video_url, filename=f'{id}_video50.mp4')

            self.delay()

        self.loot()
        self.move_vid()
