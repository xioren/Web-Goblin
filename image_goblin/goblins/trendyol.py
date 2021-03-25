from meta import MetaGoblin

# NOTE: api works sometimes...depends on product id
# TODO: find solution
# legacy: https://www.trendyol.com/assets/product/media/images/20191021/17/449253/57309150/5/5_org_zoom.jpg

class TrendyolGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'trandyol goblin'
    ID = 'trendyol'
    API_URL = 'https://api.trendyol.com/webproductgw/api/productDetail'
    IMG_BASE = 'https://cdn.dsmcdn.com'

    def __init__(self, args):
        super().__init__(args)

    def extract_base(self, url):
        '''extract base of url'''
        return self.parser.regex_sub(r'\d+/\d+_[a-z]+(_[a-z]+)?\.jpg', '', url)

    def extract_id(self, url):
        '''extract product id'''
        return self.parser.regex_search(r'(?<=p-)\d+', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'img-trendyol' in target or 'cdn.dsmcdn' in target:
                url_base = self.extract_base(target)
                ty_id = int(self.parser.regex_search(r'(?<=ty)\d+', target))

                for i in (ty_id-1, ty_id, ty_id+1):
                    new_base = self.parser.regex_sub(r'(?<=ty)\d+', str(i), url_base)
                    for j in range(1, 5):
                        urls.append(f'{new_base}{j}/{j}_org_zoom.jpg')
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                id = self.extract_id(target)
                response = self.parser.from_json(self.get(f'{self.API_URL}/{id}').content)

                if 'result' in response:
                    for image in response['result'].get('images', ''):
                        urls.append(f'{self.IMG_BASE}{image}')

            self.delay()

        for url in urls:
            parts = url.split('/')
            self.collect(url, filename=f'{parts[-2]}_{parts[-1]}'[:-4])

        self.loot()
