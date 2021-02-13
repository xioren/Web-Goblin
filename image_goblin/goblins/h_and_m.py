from meta import MetaGoblin

# NOTE: removing origin works in some cases, are there different origins?

class HMGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'h&m goblin'
    ID = 'handm'
    URL_PAT = r'source\[[\w\./]+\]'
    FULLSIZE_URL = 'https://lp2.hm.com/hmgoepprod?set=quality[100],source[{}],origin[dam]&call=url[file:/product/zoom]'

    def __init__(self, args):
        super().__init__(args)

    def extract_source(self, url):
        '''extract source path from url'''
        return self.parser.regex_search(r'source\[[\w\./]+\]', url).replace('source[', '').rstrip(']')

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'lp2.hm' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            source = self.extract_source(url)
            self.collect(self.FULLSIZE_URL.format(source), filename=self.parser.extract_filename(source))

        self.loot()
