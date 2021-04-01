from meta import MetaGoblin


class MangoGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'mango goblin'
    ID = 'mango'
    # URL_PAT = r'https?://st\.mngbcn\.com[^"\?\s]+\.jpg'
    QUERY = '?qlt=100'
    # NOTE: B, D0 == product images
    MODIFIERS = ('', '_R', '_D1', '_D2', '_D3', '_D4', '_D5', '_D6', '_D7')
    IMAGE_URL = 'https://st.mngbcn.com/rcs/pics/static'
    MAIN_API_URL = 'https://shop.mango.com/services/garments'
    OUTLET_API_URL = 'https://www.mangooutlet.com/services/garments'
    STOCK_ID_URL = 'https://shop.mango.com/services/stock-id'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id and T number from url'''
        return self.parser.regex_search(r'T\d', url), self.parser.regex_search(r'\d+_\d+', url)

    def extract_product(self, url):
        '''extract product id from url'''
        return self.parser.regex_search(r'(?<=_)\d+(?=\.)', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'mngbcn' in target:
                t, id = self.extract_id(target)

                urls.append(f'{self.IMAGE_URL}/{t}/fotos/outfit/S20/{id}-99999999_01.jpg')
                for mod in self.MODIFIERS:
                    urls.append(f'{self.IMAGE_URL}/{t}/fotos/S20/{id}{mod}.jpg')
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                init_response = self.get(target, store_cookies=True)
                self.set_cookies()

                stock_id = self.parser.from_json(self.get(self.STOCK_ID_URL).content)['key']
                self.headers.update({'stock-id': stock_id})

                if 'outlet' in target:
                    response = self.parser.from_json(self.get(f'{self.OUTLET_API_URL}/{self.extract_product(target)}').content)
                else:
                    response = self.parser.from_json(self.get(f'{self.MAIN_API_URL}/{self.extract_product(target)}').content)

                for color in response['colors']['colors']:
                    for images in color['images']:
                        if 'outlet' in target:
                            urls.append(f'{self.IMAGE_URL}{images["url"]}')
                        else:
                            for image in images:
                                urls.append(f'{self.IMAGE_URL}{image["url"]}')

            self.delay()

        for url in urls:
            if '_B' in url or '_D0' in url:
                continue
            self.collect(f'{self.parser.dequery(url)}{self.QUERY}')

        self.reset_headers()
        self.loot()
