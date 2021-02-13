from meta import MetaGoblin

# TODO:
#   - add webpage handling
#   - handle urls containing #

class IteratorGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    NAME = 'iterator goblin'
    ID = 'iterator'

    def __init__(self, args):
        super().__init__(args)
        self.block_size = self.args['step'] * 100

    def unique(self, url, other_url):
        '''check if filenames are unique'''
        if self.parser.extract_filename(url) == self.parser.extract_filename(other_url):
            return False
        return True

    def isolate_parts(self, url):
        '''seperate url into base, iterable, end'''
        return url.split('#')

    def increment_iterable(self, iterable):
        '''increment the iterable by blocksize'''
        return str(int(iterable) + self.block_size).zfill(len(iterable))

    def generate_block(self, base, iterable, end):
        '''generate block of urls to iterate over'''
        # NOTE: integer with leading zeros stripped
        real_iter = int(iterable)
        filename = ''

        for n in range(real_iter, real_iter + self.block_size, self.args['step']):
            if not self.is_unique:
                # if filenames are not unique, use iterable as filename instead
                filename = n

            self.collect(f'{base}{str(n).zfill(len(iterable))}{end}', filename=filename)

    def main(self):
        '''main iteration method'''
        self.toggle_collecton_type() # convert collection to list so that urls are ordered
        for target in self.args['targets'][self.ID]:

            base, iterable, end = self.isolate_parts(target)
            self.is_unique = self.unique(f'{base}{iterable}{end}', f'{base}{self.increment_iterable(iterable)}{end}')

            while True:
                self.logger.log(1, self.NAME, 'iterating',
                                f'block: {iterable}-{str(int(iterable) + self.block_size-self.args["step"]).zfill(len(iterable))}')
                self.generate_block(base, iterable, end)

                timed_out = self.loot(timeout=self.args['timeout'])
                if timed_out:
                    self.logger.log(1, self.NAME, 'timed out', f'after {self.args["timeout"]} attempts')
                    break
                else:
                    iterable = self.increment_iterable(iterable)
                    self.new_collection()
