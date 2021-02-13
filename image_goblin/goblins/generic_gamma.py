from meta import MetaGoblin

# NOTE: scaling with q=100 does not affect quality of original image, only the
# the quality of the re-encode --> images are still noisy and somewhat blurry
# TODO: this could really use a better approach

class GammaGoblin(MetaGoblin):
    '''handles: Demandware
    docs: https://documentation.b2c.commercecloud.salesforce.com/DOC1/index.jsp
    --> dw.content --> MediaFile
    accepts:
        - image
        - webpage
    generic backend for:
        - boux avenue
        - envii
        - eres
        - etam
        - intimissimi
        - jennyfer
        - livy
        - marlies dekkers
        - only
        - sandro
        - springfield
        - tezenis
        - vila
        - womens secret
    '''

    NAME = 'gamma goblin'
    ID = 'gamma'
    URL_PAT = r'[^"\s;]+demandware[^"\s;]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def extract_parts(self, url):
        '''split the url into id, end'''
        return self.parser.regex_split(self.ITER_PAT, url)

    def isolate(self, url):
        '''isolate the end of the url'''
        return self.parser.regex_search(r'(?<=/)[^/]+\.jpe?g', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'image' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            if not self.parser.regex_search(f'(?:{self.IMG_PAT})', url, capture=False):
                continue

            id, url_end = self.extract_parts(self.isolate(url))
            for mod in self.MODIFIERS:
                self.collect(f'{self.URL_BASE}{id}{mod}{self.parser.dequery(url_end)}{self.QUERY}')

        self.loot()
