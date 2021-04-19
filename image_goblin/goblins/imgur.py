from meta import MetaGoblin


# QUESTION: will client id work universaly?


class ImgurGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'imgur goblin'
    ID = 'imgur'
    BASE_URL = 'https://i.imgur.com/'
    API_URL = 'https://api.imgur.com/post/v1'

    def __init__(self, args):
        super().__init__(args)

    def extract_album_id(self, url):
        return self.parser.dequery(url).split('/')[-1]

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

                album_id = self.extract_album_id(target)

                response = self.parser.from_json(self.get(f'{self.API_URL}/albums/{album_id}?client_id=546c25a59c58ad7&include=media').content)
                for item in response.get('media', ''):
                    urls.append(item['url'])

            self.delay()

        for url in urls:
            self.collect(self.upgrade(url))
            # NOTE: get both gif and mp4 versions of file
            if '.gif' in url:
                self.collect(self.upgrade(url.replace('.gif', '.mp4')))
            elif '.mp4' in url:
                self.collect(self.upgrade(url.replace('.mp4', '.gif')))

        self.loot()
