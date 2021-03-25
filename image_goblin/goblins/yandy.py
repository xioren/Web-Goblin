from meta import MetaGoblin


class YandyGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'yandy goblin'
    ID = 'yandy'
    # URL_PAT = r'https?://assets\.yandycdn\.com/Products/[^-]+-\d+\.jpg'
    API_URL = 'https://andromeda.yandy.com/api/v1.1'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'assets.yandycdn' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                parts = target.replace('https://', '').split('/')
                urls.append(f'{parts[0]}/HiRez/{parts[2]}')
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                product_id = self.parser.regex_search(r'(?<=data-product-id=")[^"]+', self.get(target).content)
                response = self.parser.from_json(self.get(f'{self.API_URL}/products/{product_id}/images').content)

                for image in response['data']:
                    urls.append(image['hi_rez'])

            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
