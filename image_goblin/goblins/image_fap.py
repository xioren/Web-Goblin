from meta import MetaGoblin


class ImageFapGoblin(MetaGoblin):
    '''accepts:
        - webpage
    '''

    NAME = 'image fap goblin'
    ID = 'imagefap'
    URL_PAT = r'https?://cdn\.imagefap\.com/images/full/[^"\s<]+'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'cdn.imagefap' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                for link in self.parser.extract_by_tag(self.get(f'{self.parser.dequery(target)}?view=2').content, {'a': 'href'}):
                    if '/photo/' in link:
                        urls.extend(self.parser.extract_by_regex(self.get(f'https://www.imagefap.com{link}').content, self.URL_PAT))

            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
