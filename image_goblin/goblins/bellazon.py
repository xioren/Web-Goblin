from meta import MetaGoblin


class BellazonGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'bellazon goblin'
    ID = 'bellazon'
    BASE_URL = 'https://www.bellazon.com/'
    URL_PAT = r'https?://www\.bellazon\.com/main/uploads/[^"]+'

    def __init__(self, args):
        super().__init__(args)

    def extract_filename(self, url):
        '''for bellazon hosted content, remove hash and return real filename'''
        if 'main/uploads' in url:
            return '.'.join(url.split('.')[:-3]).split('/')[-1]
        else: # third party host
            return ''

    def extract_topic(self, url):
        '''extract thread topic'''
        return self.parser.regex_search(fr'(?<=topic/)[^/]+', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'main/uploads' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                thread_url = f'{self.BASE_URL}main/topic/{self.extract_topic(target)}'
                response = self.get(thread_url)
                pages = int(self.parser.regex_search(r'(?<="pageEnd":\s)\d', response.content))

                urls.extend(self.parser.extract_by_tag(response.content, {'img': 'src'})) # third party hosts
                urls.extend(self.parser.extract_by_regex(response.content, self.URL_PAT)) # bellazon hosted

                if pages > 1:
                    for n in range(2, pages+1):
                        response = self.get(f'{thread_url}/page/{n}')
                        urls.extend(self.parser.extract_by_tag(response.content, {'img': 'src'}))
                        urls.extend(self.parser.extract_by_regex(response.content, self.URL_PAT))

            self.delay()

        for url in urls:
            if '.thumb' not in url:
                self.collect(self.parser.auto_format(url), filename=self.extract_filename(url))

        self.loot()
