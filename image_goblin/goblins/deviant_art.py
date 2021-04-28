from meta import MetaGoblin


class DeviantArtGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'deviant art goblin'
    ID = 'deviantart'
    API_URL = 'https://www.deviantart.com/_napi/shared_api/deviation/extended_fetch?deviationid={}&username={}&type={}&include_session=false'

    def __init__(self, args):
        super().__init__(args)

    def parse_url(self, url):
        '''parse post information from url'''
        return self.parser.dequery(url).split('/')[-3:]

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:

            if 'images-wixmp' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                self.collect(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                user, type, deviation = self.parse_url(target)

                response = self.parser.from_json(self.get(self.API_URL.format(deviation.split('-')[-1], user, type)).content)

                if response['deviation']['isDownloadable']:
                    self.collect(response['deviation']['media']['baseUri'] + '?token=' + response['deviation']['media']['token'][0],
                                 filename=response['deviation']['media']['prettyName'])
                else:
                    self.collect(response['deviation']['media']['baseUri'] + '/'
                                 + self.parser.regex_sub(r'q_\d+', 'q_100', response['deviation']['media']['types'][-1]['c'])
                                 + '?token=' + response['deviation']['media']['token'][0],
                                 filename=response['deviation']['media']['prettyName'])

        self.loot()
