from meta import MetaGoblin


class TisjaDamenGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'tisja damen goblin'
    ID = 'tisjadamen'
    URL_PAT = r'/images/magictoolbox_cache/[^"\s]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''seperate image from rest url'''
        return self.parser.regex_search(r'(?<=/)[^/]+$', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'images' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            image = self.trim(url)

            for n in range(1, 4):
                self.collect(f'https://tisjadamen.com/images/detailed/{n}/{image}')

        self.loot()
