from meta import MetaGoblin


# NOTE: now uses magento api but no conformity in urls


class FredericksGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'fredericks goblin'
    ID = 'fredericks'
    URL_PAT = r'https?:[^"\s\n]+media\\?/catalog\\?/product\\?/[^"\s\n]+\.jpe?g'
    QUERY = '?quality=100'


    def __init__(self, args):
        super().__init__(args)


    def trim(self, url):
        '''remove scaling from url'''
        return self.parser.regex_sub(r'/(custom_)?cache.*?(?=/\w/\w/)', '', url)


    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:

            if 'media/catalog' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(self.parser.dequery(target))
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()
                
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            self.collect(self.trim(url) + self.QUERY)

        self.loot()
