from meta import MetaGoblin


class RedGifsGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'redgifs goblin'
    ID = 'redgifs'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:
            if 'thcf' in target:
                self.collect(target)
            else:
                response = self.get(target).content

                if 'gifdeliverynetwork' in target:
                    url = self.parser.regex_search(r'(?<=mp4Source" src=")[^"]+', response).replace('-mobile', '')
                else:
                    url = self.parser.regex_search(r'(?<=og:video" content=")[^"]+', response).replace('-mobile', '')

                self.collect(url)
                self.collect(url.replace('.mp4', '-size_restricted.gif'))

        self.loot()
