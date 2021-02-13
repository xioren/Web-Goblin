from meta import MetaGoblin


# misc: '/noscript'


class ImgurGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'imgur goblin'
    ID = 'imgur'
    BASE_URL = 'https://i.imgur.com/'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        return self.parser.regex_sub(r'(/embed|#).?$', '', self.parser.dequery(url))

    def upgrade(self, url):
        '''upgrade image size'''
        filename  = self.parser.extract_filename(url)

        if len(filename) == 8:
            ext = self.parser.extension(url)
            # IDEA: could skip the len check and just return url[:7]
            url = f'{self.BASE_URL}{filename[:-1]}{ext}'.replace('jpeg', 'jpg')

        return url.replace('m.imgur', 'i.imgur')

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'i.imgur' in target or 'm.imgur' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                if '/r/' in target:

                    matches = self.parser.extract_by_regex(self.get(self.trim(target)).content,
                                                           r'(?<=image\s{15}:\s){[^\n]+}(?=,\n)')
                    for match in matches:
                        items = self.parser.load_json(match)
                        urls.append(f'{self.BASE_URL}{items["hash"]}{items["ext"]}')
                else:
                    matches = self.parser.extract_by_regex(self.get(self.trim(target)).content,
                                                           r'(?<=image\s{15}:\s){[^\n]+}(?=,\n)')
                    for match in matches:
                        items = self.parser.load_json(match)
                        if items['is_album'] == True:
                            for item in items['album_images']['images']:
                                urls.append(f'{self.BASE_URL}{item["hash"]}{item["ext"]}')
                        else:
                            urls.append(f'{self.BASE_URL}{items["hash"]}{items["ext"]}')

                    if not urls: # sign in probably required -> try bypass
                        self.logger.log(1, self.NAME, 'bypassing sign in gate')

                        if '/a/' in target:
                            matches = self.parser.extract_by_regex(self.get(f'{self.trim(target)}/embed').content,
                                                                   r'(?<=images\s{6}:\s){[^\n]+}(?=,\n)')
                            for match in matches:
                                items = self.parser.load_json(match)

                                for item in items.get('images', ''):
                                    urls.append(f'{self.BASE_URL}{item["hash"]}{item["ext"]}')
                        else:
                            response = self.get(target)
                            urls.append(self.parser.regex_search(r'og:image"\s+content="[^"\?]+', response.content).split('="')[-1])
                            if 'og:video' in response.content:
                                urls.append(self.parser.regex_search(r'og:video"\s+content="[^"\?]+', response.content).split('="')[-1])

            self.delay()

        for url in urls:
            self.collect(self.upgrade(url))
            # NOTE: get both gif and mp4 versions of file
            if '.gif' in url:
                self.collect(self.upgrade(url.replace('.gif', '.mp4')))
            elif '.mp4' in url:
                self.collect(self.upgrade(url.replace('.mp4', '.gif')))

        self.loot()
