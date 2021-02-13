from meta import MetaGoblin


class GiphyGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'giphy goblin'
    ID = 'giphy'
    IMAGE_BASE_URL = 'https://i.giphy.com/media'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:
            if 'i.giphy' in target:
                self.collect(target.replace('.webp', '.gif'), filename=target.split('/')[-2])
                self.collect(target.replace('.webp', '.mp4').replace('.gif', '.mp4'), filename=target.split('/')[-2])
            else:
                if 'media' in target:
                    slug = target.split('/')[-2]
                else:
                    slug = target.split('-')[-1]

                self.collect(f'{self.IMAGE_BASE_URL}/{slug}/giphy.gif', filename=slug)
                self.collect(f'{self.IMAGE_BASE_URL}/{slug}/giphy.mp4', filename=slug)

        self.loot()
