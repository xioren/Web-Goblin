from meta import MetaGoblin


class BehanceGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'behance goblin'
    ID = 'behance'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'mir-s3-cdn' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(self.parser.regex_sub(r'(?<=modules/)[^/]+', 'source', target))
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                self.headers.update({'X-Requested-With': 'XMLHttpRequest',
                                     'Cookie': 'ilo0=true'})

                response = self.parser.load_json(self.get(self.parser.dequery(target)).content)
                if 'view' in response:
                    for module in response['view']['project']['modules']:
                        if 'components' in module:
                            for component in module['components']:
                                urls.append(component['sizes']['source'])
                        elif 'sizes' in module:
                            urls.append(module['sizes']['original'])

            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
