from meta import MetaGoblin


# NOTE: unfinished


class DeviantArtGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'deviant art goblin'
    ID = 'deviantart'
    URL_PAT = r'(?<=og:image"\scontent=")https?://images-wixmp[^"\s]+'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''remove scaling'''
        return self.parser.regex_sub(r'/v1/[^\?]+(?=\?)', '', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if '.jpg' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            self.collect(self.trim(url), filename=self.parser.regex_sub(r'_[a-z\d]+-pre', '', self.parser.extract_filename(url)))

        self.loot()
