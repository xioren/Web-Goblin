from meta import MetaGoblin


# NOTE: uses different urls structure depending on region
# alternate: https://www.hunkemoller.co.uk/on/demandware.static/-/Sites-hkm-master/default/images/large/
# alternate: https://hunkemoller.by/media/img/hkm/


class HunkemollerGoblin(MetaGoblin):

    NAME = 'hunkemoller goblin'
    ID = 'hunkemoller'
    MODIFIERS = [f'_{n}' for n in range(1, 10)]
    URL_BASE = 'https://images-hunkemoller.akamaized.net/original/'

    def __init__(self, args):
        super().__init__(args)
        self.URL_TYPES = self.parser.regex_pattern('(?:akamaized|img/hkm|demandware)')
        self.ITER_PAT= self.parser.regex_pattern(r'_\d(?=\.jpg)')
        self.IMG_PAT = self.parser.regex_pattern(r'(?:\d+_\d(_normal)?\.jpg)')
        self.URL_PAT = self.parser.regex_pattern(r'https?://images-hunkemoller\.akamaized.net/[^"\s]+' \
                                                 r'|https?://hunkemoller\.[a-z]/media/img/hkm/[^"\s]+' \
                                                 r'|https://www\.hunkemoller\.[^"\s]+demandware[^"\s]+')

    def extract_parts(self, url):
        '''split the url into id, end'''
        return self.parser.regex_split(self.ITER_PAT, url.replace('_normal', ''))

    def isolate(self, url):
        '''isolate the end of the url'''
        return self.parser.regex_search(r'(?<=/)[^/]+\.jpe?g', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if self.parser.regex_search(self.URL_TYPES, target, capture=False):
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            # NOTE: finds way too many urls. consider new approach.
            if not self.parser.regex_search(self.IMG_PAT, url, capture=False):
                continue

            id, url_end = self.extract_parts(self.isolate(url))

            for mod in self.MODIFIERS:
                self.collect(f'{self.URL_BASE}{id}{mod}{self.parser.dequery(url_end)}')

        self.loot()
