from logging import Logger


logger = Logger(False, False, False)

# IDEA: add keep flag for exporting links to txt

class HungryGoblin:

    NAME = 'hungry goblin'

    def __init__(self):
        self.meal = set()
        logger.log(0, self.NAME, 'deployed')

    def main(self):
        while True:
            bite = input(f'[{self.NAME}] <feed> ')
            if bite == '':
                break
            self.meal.add(bite)

        logger.log(0, self.NAME, 'digesting')
        return self.meal
