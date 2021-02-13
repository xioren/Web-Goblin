from meta import MetaGoblin

# BUG: currently getting gzip EOF errors
# NOTE: same as kitess

class BrownieGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'brownie goblin'
    ID = 'brownie'
    URL_PAT = r'https?://www\.browniespain\.com/\d+-thickbox_default/[a-z\d\-]+\.jpg'
    URL_BASE = 'https://www.browniespain.com'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        return self.parser.regex_search(r'(?<=\.com/)\d+', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if '.jpg' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            id = self.extract_id(url)
            self.collect(f'{self.URL_BASE}/{id}/{id}.jpg')

        self.loot()
