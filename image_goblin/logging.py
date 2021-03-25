from math import floor
from itertools import cycle
from os import get_terminal_size


class Logger:
    '''Program Output'''

    def __init__(self, verbose, silent, nodl):
        self.verbose = verbose
        self.silent = silent
        self.nodl = nodl
        self.logged = [] # NOTE: keep track of log once logs
        self.spinner = cycle(['#-----', '-#----', '--#---', '---#--', '----#-',
                              '-----#', '----#-', '---#--', '--#---', '-#----'])

    def clear_line(self):
        '''clear the current terminal line'''
        try:
            print(' ' * (get_terminal_size().columns-1), end='\r')
        except OSError:
            # NOTE: ioctl error when redirecting output
            pass

    def log(self, level, caller, msg, info='', clear=False, once=False):
        '''logging messages
        - level 0: basic
        - level 1: normal
        - level 2: verbose
        '''
        if clear:
            self.clear_line()
        if level == 1 and self.silent:
            pass
        elif level == 2 and not self.verbose or self.silent:
            pass
        else:
            output = f'[{caller}] <{msg}> {info}'
            if output not in self.logged:
                print(output)
                if once:
                    self.logged.append(output)

    def progress(self, caller, msg, current, total, units=''):
        '''progress bar'''
        if not (self.silent or self.nodl):
            self.clear_line()
            bar = '#' * floor(current/total * 20)
            print(f'[{caller}] <{msg}> [{bar.ljust(20, " ")}] {current} of {total} {units}', end='\r')

    def spin(self):
        '''activity spinner'''
        if not (self.verbose or self.silent):
            print(f'[{next(self.spinner)}]', end='\r')
