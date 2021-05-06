from meta import MetaGoblin


class SquarespaceGoblin(MetaGoblin):
    '''docs: https://developers.squarespace.com/url-queries
    accepts:
        - image*
        - webpage
    '''

    NAME = 'squarespace goblin'
    ID = 'squarespace'
    QUERY = '?format=original'
    IMG_PAT = r'https://images\.squarespace-cdn\.com[^"]+'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:

            if 'squarespace-cdn.' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                self.collect(self.parser.dequery(target) + self.QUERY)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                response = self.parser.from_json(self.get(self.parser.dequery(target).replace('/#/', '/') + '?format=json').content)

                if response.get('items'):
                    for item in response['items']:
                        self.collect(item['assetUrl'] + self.QUERY, filename=item['filename'])
                elif response.get('item'):
                    # NOTE: response does not contain all images in json -> parse body
                    self.collect(response['item']['assetUrl'] + self.QUERY)
                    for url in self.parser.extract_by_regex(response['item'].get('body', ''), self.IMG_PAT):
                        self.collect(url + self.QUERY)
                else:
                    # NOTE: response does not contain any images in json -> parse body
                    for url in self.parser.extract_by_regex(response.get('mainContent', ''), self.IMG_PAT):
                        self.collect(url + self.QUERY)

            self.delay()

        self.loot()
