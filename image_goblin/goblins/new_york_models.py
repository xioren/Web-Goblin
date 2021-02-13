from meta import MetaGoblin

# NOTE: works for la models too

class NewYorkModelsGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'new york models goblin'
    ID = 'newyorkmodels'
    IMAGE_URL_BASE = 'https://s3.amazonaws.com/media-ima002.globaltalentsystems.com/{}/1200'
    VIDEO_URL_BASE = 'https://s3.amazonaws.com/media-vid000.globaltalentsystems.com/{}'
    API_URL = 'http://www.newyorkmodels.com/control/portfolio_get.php?initi=1&model_id=&the_type=&port_id=&ref={}'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'globaltalentsystems' in target:
                urls.append(self.parser.regex_sub(r'\d+(?=/\d+_)', '1200', target))
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                init_response = self.get(target).content
                portfolio_id = self.parser.regex_search(r"(?<=var\sref\s=\s')[^']+", init_response)

                response = self.get(self.API_URL.format(portfolio_id))

                model_id = self.parser.regex_search(r'(?<=|)\d+(?=|)', response.content)
                relatives = self.parser.extract_by_regex(response.content, r'[\w\.\-]+\.\w+(?=<BR>)')
                video_relatives = self.parser.extract_by_regex(response.content, r'\d+(?=\.flv)')

                for rel in relatives:
                    urls.append(f'{self.IMAGE_URL_BASE.format(model_id)}/{rel}')

                if video_relatives:
                    for rel in video_relatives:
                        urls.append(f'{self.VIDEO_URL_BASE.format(model_id)}/{rel}.mp4')


            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
