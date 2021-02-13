from meta import MetaGoblin


# FIXME: data-original (and maybe others) seems to be the source of +filename+.html downloads


class OmegaGoblin(MetaGoblin):
    '''handles: all urls that did not match a specific goblin
    accepts:
        - image
        - webpage
    '''

    NAME = 'generic goblin'
    ID = 'generic'

    FILETYPES = r'\.(jpe?g|png|gif|mp4|web[pm]|tiff?|mov|svg|bmp|exif)'

    def __init__(self, args):
        super().__init__(args)
        self.URL_PAT = self.parser.regex_pattern(fr'[^"\s\n\'\;,=]+?{self.FILETYPES}(\?[^"\s\n\'\|)]+)?', ignore=True)
        self.IMG_PAT = self.parser.regex_pattern(f'(?:{self.FILETYPES}|/upload/|/images?/)', ignore=True) # QUESTION: too general?
        self.ATTR_PAT = self.parser.regex_pattern(r'(?:src(?![a-z])|data(?![a-z\-])|data-(src(?!set)|lazy(?!-srcset)|url|original)' \
                                                  r'|content(?![a-z\-])|hires(?![a-z\-]))')
        self.TAG_PAT = self.parser.regex_pattern('(?:a(?![a-z])|ima?ge?|video|source|div)')

    def format(self, url):
        '''format a url either automatically or via user input'''
        if self.args['format']:
            return self.parser.user_format(url)
        elif self.args['noup']:
            return url
        else:
            return self.parser.auto_format(url)

    def find_urls(self, url):
        '''find and collect urls'''
        urls = []
        elements = self.parser.extract_by_tag(self.get(url).content)

        for tag in elements:
            if self.parser.regex_startswith(self.TAG_PAT, tag):
                for attribute in elements[tag]:
                    if self.parser.regex_startswith(self.ATTR_PAT, attribute):
                        urls.extend(elements[tag][attribute])

        for url in urls:
            self.collect(self.format(url), filename=self.args['filename'])

    def find_urls_greedy(self, url):
        '''greedily find and collect urls'''
        urls = self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)

        for url in urls:
            if '.php?img=' in url:
                url = url.split('.php?img=')[1]
            self.collect(self.format(url), filename=self.args['filename'])

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:

            if self.parser.regex_search(self.IMG_PAT, target):
                self.collect(self.format(target))
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                if self.args['greedy']:
                    self.find_urls_greedy(target)
                else:
                    self.find_urls(target)

            self.delay()

        self.loot()
