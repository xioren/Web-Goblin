import urllib.parse

from meta import MetaGoblin


class VSCOGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'vsco goblin'
    ID = 'vsco'
    API_URL = 'https://vsco.co/api/3.0/medias/profile?site_id={}&limit={}&cursor={}'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'aws.' in target or 'aws-' in target:
                urls.append(self.parser.sanitize(target))
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                init_response = self.get(target)
                site_id = self.parser.regex_search(r'(?<="siteId":)\d+', init_response.content)
                cursor = ''
                self.headers.update({'Authorization': 'Bearer 7356455548d0a1d886db010883388d08be84d0c9'})

                while True:
                    response = self.parser.load_json(self.get(self.API_URL.format(site_id, 100, urllib.parse.quote(cursor))).content)

                    for item in response.get('media', ''):
                        urls.append(item['image'].get('responsive_url', ''))

                    cursor = response.get('next_cursor', '')
                    if not cursor:
                        break
            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
