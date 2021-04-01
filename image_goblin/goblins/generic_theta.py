from meta import MetaGoblin


class ThetaGoblin(MetaGoblin):
    '''handles: shopify
    docs: https://shopify.dev/docs/themes/liquid/reference/filters/url-filters#img_url,
          https://shopify.dev/docs/admin-api/rest/reference/products/product-image#index-2021-01
    accepts:
        - image*
        - webpage
    generic back-end for:
        - arnhem
        - bamba swim
        - bluebella
        - bordelle
        - caro swim
        - cecilie copenhagen
        - dora larsen
        - else
        - fae
        - faithful the brand
        - fashion nova
        - five dancewear
        - fleur du mal
        - for love and lemons
        - fortnight
        - gooseberry
        - hanne bloch
        - honey birdette
        - juillet
        - kiki de montparnasse
        - lounge
        - myla
        - par femme
        - seamless basic
        - skatie
        - skin
        - sommer swim
        - the great eros
        - triangl
        - underprotection
        - vitamin a
    '''

    NAME = 'theta goblin'
    ID = 'theta'
    QUERY = 'https://{}/products/{}.js'

    def __init__(self, args):
        super().__init__(args)
        self.HASH_PAT = self.parser.regex_pattern(r'_[a-z\d]+(\-[a-z\d]+){4}')
        self.CROPPING_PAT = self.parser.regex_pattern(r'-/format/auto/-/preview/\d+x\d+/-/quality/[a-z]+/|_[a-z]+(?=\.)')

    def trim(self, url):
        '''remove variant hash'''
        return self.parser.regex_sub(self.HASH_PAT, '', url)

    def decrop(self, url):
        '''remove cropping'''
        return self.parser.regex_sub(self.CROPPING_PAT, '', url)

    def extract_vendor(self, url):
        '''extract shopify vendor url'''
        return self.parser.regex_search(r'(?<=://)?[\-\w]+(\.[a-z]+)+', url)

    def extract_product(self, url):
        '''extract shopify product tag'''
        return self.parser.regex_search(r'(?<=products/)[\-\w]+', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'cdn.shopify' in target or 'i.shgcdn' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                if 'i.shgcdn' in url:
                    urls.append(self.decrop(target))
                else:
                    urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                vendor = self.extract_vendor(target)
                product = self.extract_product(target)
                if product:
                    response = self.parser.from_json(self.get(self.QUERY.format(vendor, product)).content)
                    urls.extend(response.get('images', ''))

            self.delay()

        for url in urls:
            if self.parser.regex_search(self.HASH_PAT, target, capture=False):
                # NOTE: collect de-hashed url if an alternate hash is present
                self.collect(self.trim(url), clean=True)
            self.collect(url, clean=True)

        self.loot()
