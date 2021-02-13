from meta import MetaGoblin


class ListalGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'listal goblin'
    ID = 'listal'
    BASE_URL = 'https://www.listal.com'
    IMG_URL = 'https://iv1.lisimg.com/image'
    ID_PAT = r'(?<=radioimageids\[)\d+'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''exract image number'''
        return self.parser.regex_search(r'(?<!com/)\d{6,}(?![a-z])', url)

    def extract_name(self, url):
        '''extract profile name'''
        return self.parser.regex_search(fr'(?<={self.BASE_URL}/)[\w\-]+', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'lisimg' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                if 'viewimage' in target:
                    urls.append(f'{self.IMG_URL}/{self.extract_id(target)}/36800full.jpg')
                else:
                    self.logger.log(2, self.NAME, 'looting', target)
                    self.logger.spin()
                    
                    name = self.extract_name(target)
                    profile_url = f'{self.BASE_URL}/{name}'
                    ids = self.parser.extract_by_regex(self.get(f'{profile_url}/pictures').content, self.ID_PAT)
                    for id in ids:
                        urls.append(f'{self.IMG_URL}/{id}/36800full.jpg')

                    n = 2
                    while True:
                        ids = self.parser.extract_by_regex(self.get(f'{profile_url}/pictures/{n}').content, self.ID_PAT)
                        if not ids:
                            break
                        for id in ids:
                            urls.append(f'{self.IMG_URL}/{id}/36800full.jpg')
                        n += 1

            self.delay()

        for url in urls:
            if 'thumb' in url:
                self.collect(f'{self.IMG_URL}/{self.extract_id(url)}/36800full.jpg', filename=self.extract_id(url))
            else:
                self.collect(self.parser.regex_sub(r'\d+full', '3800full', url), filename=self.extract_id(url))

        self.loot()
