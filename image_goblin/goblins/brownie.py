from meta import MetaGoblin

# NOTE: for json response containing html
# self.headers.update({'accept': 'application/json',
#                      'x-requested-with': 'XMLHttpRequest',
#                      'content-type': 'application/x-www-form-urlencoded'})
# url = "https://www.browniespain.com/en/index.php?controller=product&id_product={id}"
# self.post(url, {"ajax": 1, "action": "refresh"})
# NOTE: same as kitess


class BrownieGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'brownie goblin'
    ID = 'brownie'
    URL_PAT = r'https?://www\.browniespain\.com/([a-z]+/)?\d+-thickbox_default/[a-z\d\-]+\.jpg'
    URL_BASE = 'https://www.browniespain.com'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        return self.parser.regex_search(r'(?<=/)\d+(?=-)', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if '.jpg' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(self.parser.regex_sub("#.+", '', target)).content, self.URL_PAT))

            self.delay()

        for url in urls:
            id = self.extract_id(url)
            self.collect(url.replace('-thickbox_default', ''), filename=id)

        self.loot()
