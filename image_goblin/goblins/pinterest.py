from urllib.parse import quote

from meta import MetaGoblin


# NOTE: max page size == 250


class PinterestGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'pinterest goblin'
    ID = 'pinterest'
    BASE_URL = 'https://www.pinterest.com'
    PIN_RESOURCE_URL = '/resource/PinResource/get/?source_url=/{}/&data={{"options":{{"id":"{}"}},"context":{{}}}}'
    BOARD_RESOURCE_URL = '/resource/BoardResource/get/?source_url=/{}/&data={{"options":{{"username":"{}","slug":"{}"}},"context":{{}}}}'
    BOARD_MEDIA_URL = '/resource/BoardFeedResource/get/?source_url=/{}/&data={{"options":{{"board_id":"{}","page_size":250}},"context":{{}}}}'
    BOOKMARKED_BOARD_MEDIA_URL = '/resource/BoardFeedResource/get/?source_url=/{}/&data={{"options":{{"board_id":"{}","page_size":250,"bookmarks":["{}"]}},"context":{{}}}}'

    def __init__(self, args):
        super().__init__(args)

    def extract_info(self, url):
        '''extract board source url, username, and slug'''
        url = url.rstrip('/').replace('//', '')

        if url.count('/') == 2:
            username, slug = url.split('/')[1:]
        else:
            username, slug = '', ''

        path = f'{username}/{slug}'
        return path, username, slug

    def extract_urls(self, json):
        '''extract urls from json response'''
        urls = []
        for entry in json['resource_response']['data']:
            if entry.get('images'):
                urls.append(entry['images']['orig']['url'])

        return urls

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'i.pinimg' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                if '/pin/' in target:
                    path, _, slug = self.extract_info(target)

                    response = self.parser.load_json(self.get('{}{}'.format(self.BASE_URL, self.PIN_RESOURCE_URL.format(path, slug))).content)
                    urls.append(response['resource_response']['data']['images']['736x']['url'])
                else:
                    path, username, slug = self.extract_info(target)
                    if slug:
                        init_response = self.parser.load_json(self.get('{}{}'.format(self.BASE_URL, self.BOARD_RESOURCE_URL.format(path, username, slug))).content)
                        board_id = init_response['resource_response']['data']['id']
                        # pin_count = int(init_response['resource_response']['data']['pin_count'])

                        media_response = self.parser.load_json(self.get('{}{}'.format(self.BASE_URL, self.BOARD_MEDIA_URL.format(path, board_id))).content)
                        bookmark = media_response['resource_response'].get('bookmark')
                        urls.extend(self.extract_urls(media_response))

                        if bookmark: # more images to load (page scroll)
                            while True:
                                media_response = self.parser.load_json(self.get('{}{}'.format(self.BASE_URL, self.BOOKMARKED_BOARD_MEDIA_URL.format(path, board_id, bookmark))).content)
                                bookmark = media_response['resource_response'].get('bookmark')
                                urls.extend(self.extract_urls(media_response))

                                if not bookmark: # end of board
                                    break
                                self.delay()
                    else:
                        # probably a profile url was entered
                        self.logger.log(2, self.NAME, 'ERROR', 'board not found')

            self.delay()

        for url in urls:
            self.collect(self.parser.regex_sub(r'\d+x', 'originals', url))

        self.loot()
