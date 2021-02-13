from meta import MetaGoblin

# TODO: add site specific iteration and scannable flag

class ThetaGoblin(MetaGoblin):
    '''handles: shopify
    docs: https://help.shopify.com/en/manual/products/product-media
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
    URL_PAT = r'cdn\.shopify\.com/s/files/[^"\s\n]+'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''remove variant hash'''
        return self.parser.regex_sub(r'_[a-z\d]+(\-[a-z\d]+){4}', '', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'cdn.shopify' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            url = url.replace('_small', '').replace('_grande', '')
            # NOTE: collect both the url as is and the de-hashed url if hash is present
            self.collect(url, clean=True)
            self.collect(self.trim(url), clean=True)

        self.loot()
