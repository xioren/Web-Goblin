from meta import MetaGoblin


# NOTE: fmt=png works as well


class IotaGoblin(MetaGoblin):
    '''handles: Urban Outfitters API with Adobe Dynamic Media Image Serving and Image Rendering API (scene7) backend
    accepts:
        - image
        - webpage
    generic backend for:
        - anthropologie
        - free people
        - urban outfitters
    '''

    NAME = 'iota goblin'
    ID = 'iota'
    # NOTE: as high as scl=.7 has worked in some cases
    QUERY = '?fmt=jpeg&qlt=100&scl=1'
    # FALLBACK_QUERY = '?fmt=jpeg&qlt=100&scl=1.3'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return self.parser.regex_search(r'\w+(_\w+)?(?=_\w+)', self.parser.dequery(url))

    def extract_base(self, url):
        '''extract url base'''
        return self.parser.regex_sub(r'/\d+_\d+_[A-Za-z]', '', self.parser.dequery(url)).rstrip('/')

    def extract_product(self, url):
        '''extract product from url'''
        return self.parser.dequery(url).rstrip('/').split('/')[-1]

    def set_auth_tokens(self, tokens):
        '''extract auth and reauth tokens from response cookie'''
        self.auth_token = tokens['authToken']
        self.reauth_token = tokens['reauthToken']

    def reauthorize(self):
        '''get new auth and reauth tokens'''
        auth_tokens = self.parser.load_json(self.post(self.AUTH_API_URL, data={"reauthToken": self.reauth_token}).content)
        self.set_auth_tokens(auth_tokens)
        self.headers.update({'authorization': f'Bearer {self.auth_token}'})

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            target = self.parser.regex_sub('(eu)?images.urbanoutfitters', 's7g10.scene7', target)
            if 'scene7' in target:
                # NOTE: singapore uses different cdn
                if 'i.localised' in target:
                    self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                id = self.extract_id(target)
                self.url_base = self.extract_base(target)

                for mod in self.MODIFIERS:
                    urls.append(f'{self.url_base}/{id}{mod}{self.QUERY}')
            else:
                # FIXME: currently returns 403 forbidden on eu
                if 'en-sg' in target or 'en-gb' in target:
                    self.logger.log(2, self.NAME, 'WARNING', 'webpage urls not supported', once=True)
                else:
                    self.logger.log(2, self.NAME, 'looting', target)
                    self.logger.spin()

                    init_response = self.get(target, store_cookies=True)
                    if init_response.code == 200:
                        self.set_auth_tokens(self.parser.load_json(self.parser.unquote(self.cookie_value('urbn_auth_payload'))))

                        self.headers.update(
                            {
                                'Accept': 'application/json',
                                'x-urbn-site-id': self.cookie_value('siteId'),
                                'x-urbn-channel': 'web',
                                'x-urbn-currency': self.cookie_value('urbn_currency'),
                                'x-urbn-language': init_response.info['locale'].replace('_', '-'),
                                'authorization': f'Bearer {self.auth_token}'
                            }
                        )

                        response = self.parser.load_json(self.get(self.API_URL.format(self.extract_product(target))).content)

                        # QUESTION: isinstance checks necessary?
                        if isinstance(response, dict) and response.get('code') == 'EXPIRED_TOKEN':
                            self.logger.log(2, self.NAME, 'reauthorizing')
                            self.reauthorize()
                            response = self.parser.load_json(self.get(self.API_URL.format(self.extract_product(target))).content)

                        if isinstance(response, list) and 'skuInfo' in response[0]:
                            for slice in response[0]['skuInfo']['primarySlice']['sliceItems']:
                                url = '_'.join(slice['swatchUrl'].split('_')[:-1])

                                for image in slice.get('images', ''):
                                    urls.append(f'{url}_{image}{self.QUERY}')
            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
