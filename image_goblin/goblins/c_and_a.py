from meta import MetaGoblin


# NOTE: can scale with c_scale,h_5058,q_100


class CAGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'c&a goblin'
    ID = 'canda'
    URL_PAT = r'https?://www\.c-and-a\.com/productimages/[^"\s]+/v[^"\s]+-0[1-9]\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'productimages' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            id = self.parser.regex_search(r'/\d+-\d+', url)
            for n in range(1, 6):
                self.collect(f'https://www.c-and-a.com/productimages/q_100{id}-0{n}.jpg')

        self.loot()
