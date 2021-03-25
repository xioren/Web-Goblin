from meta import MetaGoblin


class SavageXGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'savagex goblin'
    ID = 'savagex'
    # URL_PAT = r'https?://[^"\s\n]+\d-800x800\.jpg'
    API_URL = 'https://www.savagex.com/api'
    API_AUTH_URL = API_URL + '/sessions'

    def __init__(self, args):
        super().__init__(args)

    def product_id(self, url):
        '''extract product id from url'''
        return self.parser.dequery(url).split('-')[-1]

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'cdn.savagex' in target:
                urls.extend([self.parser.regex_sub(r'\d-\d+x\d+', f'{n}-1600x1600', target) for n in range(1, 7)])
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                init_response = self.get(target, store_cookies=True)
                self.set_cookies()
                # QUESTION: does this change? can storedomain be extracted from req url?
                self.headers.update({'x-api-key': 'V0X9UnXkvO4vTk1gYHnpz7jQyAMO64Qp4ONV2ygu',
                                     'x-tfg-storedomain':'www.savagex.com'})

                auth = self.get(self.API_AUTH_URL, store_cookies=True)
                self.set_cookies()

                response = self.parser.from_json(self.get(f'{self.API_URL}/products/{self.product_id(target)}').content)
                if response:
                    # BUG: doesnt return all images
                    urls.extend(response['image_view_list'])

        self.delay()

        for url in urls:
            # skip product images
            if 'laydown' in url or 'LAYDOWN' in url:
                continue

            self.collect(self.parser.regex_sub(r'\d+x\d+', '1600x1600', url).replace('-(XS-XL)', ''))

        self.loot()
