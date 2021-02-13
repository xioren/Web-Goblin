from meta import MetaGoblin


class TallyWeijlGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'tally weijl goblin'
    ID = 'tallyweijl'
    URL_PAT = r'https?://www\.tally\-weijl\.com/img/[^"\s]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if '/img/' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            self.collect(self.parser.regex_sub(r'img/\d+/\d+', 'img/1800/1800', url))

        self.loot()
