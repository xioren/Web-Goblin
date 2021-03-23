import re
import os

from logging import Logger
from parsing import Parser
from manifest import goblins


class Dispatcher:

    NAME = 'dispatcher'

    def __init__(self, args):
        self.args = args
        self.logger = Logger(self.args['verbose'], self.args['silent'], self.args['nodl'])

    def identify(self, url):
        '''match url to a specific goblin'''
        for goblin in goblins:
            if re.search(f'(?:{goblins[goblin][0]})', url, re.IGNORECASE):
                return goblin
        return 'generic'

    def dispatch(self):
        '''identify and deploy goblins'''
        if self.args['list']:
            for key in goblins:
                print(key)
            return None
        elif self.args['local']:
            local_path = self.args['local']

            if not os.path.exists(local_path):
                self.logger.log(0, self.NAME, 'ERROR', f'local path not found: {local_path}')
                return None

            with open(local_path) as file:
                urls = set(file.read().splitlines())
        elif self.args['feed']:
            goblin = goblins['hungry'][1]
            urls = goblin().main()
        else:
            urls = [self.args['url']]

        url_assignment = {}

        # NOTE: map urls to relevent goblins -> {goblin1: [urls][, goblin2: [urls]]...}
        for url in urls:
            if not Parser.valid_url(url):
                self.logger.log(0, self.NAME, 'invalid url', url)
                continue

            if self.args['goblin']:
                key = self.args['goblin']
            else:
                key = self.identify(url)

            if key in url_assignment:
                url_assignment[key].append(url)
            else:
                url_assignment[key] = [url]

        self.args['targets'] = url_assignment

        for key in url_assignment:
            try:
                goblin = goblins[key][1]
            except KeyError:
                self.logger.log(0, self.NAME, 'ERROR', f'unkown goblin "{key}" ' \
                                '-> use --list to see available goblins')
                continue
            goblin(self.args).main()
