import os

from sys import exit
from time import sleep
from shutil import move
from random import randint
from socket import timeout
from contextlib import closing
from urllib.parse import urlencode
from http.cookiejar import CookieJar
from gzip import decompress, GzipFile
from http.client import RemoteDisconnected
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from io import DEFAULT_BUFFER_SIZE, BufferedReader

from parsing import Parser
from logging import Logger
from version import __version__


class MetaGoblin:
    '''generic utility goblin inherited by all other goblins'''

    def __init__(self, args):
        self.args = args
        self.collection = set()
        self.MIN_SIZE = self.args['minsize']

        if self.args['nosort']:
            self.path_main = os.getcwd()
        elif self.args['dir']:
            self.path_main = os.path.join(os.getcwd(), self.args['dir'].replace(' ', '_'))
        else:
            self.path_main = os.path.join(os.getcwd(), 'goblin_loot', self.NAME.replace(' ', '_'))

        if self.args['mask']:
            user_agent = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36'
        else:
            user_agent = f'ImageGoblin/{__version__}'
        self.headers = {'User-Agent': user_agent,
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip'}


        self.cookie_jar = CookieJar()
        self.logger = Logger(self.args['verbose'], self.args['silent'], self.args['nodl'])
        self.parser = Parser(self.args['targets'][self.ID][0], self.args['format'],
                             self.args['ext'], self.args['filter'])

        self.make_dirs(self.path_main)
        self.logger.log(1, self.NAME, 'deployed')
    ####################################################################
    # sub classes
    ####################################################################

    class ParsedResponse:
        '''wrapper for http.client.HTTPResponse'''

        def __init__(self, response, *args, **kwargs):
            if response:
                self.code = response.code
                self.info = response.info()
                if response.info().get('Content-Encoding') == 'gzip':
                    self.content = MetaGoblin.unzip(response.read()).decode('utf-8', 'ignore')
                else:
                    self.content = response.read().decode('utf-8', 'ignore')
            else:
                self.code = ''
                self.info = ''
                self.content = '{}'

    ####################################################################
    # methods
    ####################################################################

    ####################################################################
    # miscellaneous
    ####################################################################

    def delay(self, override=None):
        '''central delay method'''
        if override:
            sleep(override)
        elif self.args['delay'] == -1:
            sleep(randint(0, 10))
        else:
            sleep(self.args['delay'])

    def move_vid(self, path=None):
        '''move video files into seperate directory'''
        if not self.args['nodl']:
            if not path:
                path = self.path_main
            vid_dir = os.path.join(path, 'vid')
            self.make_dirs(vid_dir)

            for file in os.listdir(path):
                if self.parser.extension(file) in ('.mp4', '.webm', '.mkv', '.mov', '.wmv'):
                    move(os.path.join(path, file), vid_dir)

    def make_dirs(self, *paths):
        '''creates directories'''
        if not self.args['nodl']:
            for path in paths:
                try:
                    os.makedirs(path, exist_ok=True)
                except OSError as e:
                    # NOTE: no sense in continuing if the download dir fails to make
                    # may change approach in future, exit for now
                    self.logger.log(1, self.NAME, e, 'exiting')
                    exit(5) # NOTE: input/output error

    def toggle_collecton_type(self):
        '''toggle collection type between list and set'''
        if isinstance(self.collection, list):
            self.collection = set()
        else:
            self.collection = []

    def new_collection(self):
        '''initialize a new collection'''
        self.collection.clear()

    def unzip(data):
        '''gzip decompression'''
        try:
            return decompress(data)
        except EOFError:
            return b''

    ####################################################################
    # http
    ####################################################################

    def cookie_value(self, name):
        '''return the value of a cookie from the cookie jar'''
        for cookie in self.cookie_jar:
            if cookie.name == name:
                return cookie.value

    def set_cookies(self):
        '''parse reponse headers and set cookies'''
        for cookie in self.cookie_jar:
            self.extend_cookie('Cookie', f'{cookie.name}={cookie.value}')

    def extend_cookie(self, cookie, value):
        '''add or extend a cookie'''
        if cookie not in self.headers:
            self.headers[cookie] = value
        else:
            current_values = {}
            key_val_pair = value.split('=')
            new_key = key_val_pair[0]
            new_val = '='.join(key_val_pair[1:])

            for item in self.headers[cookie].split('; '):
                key_val_pair = item.split('=')
                key = key_val_pair[0]
                val = '='.join(key_val_pair[1:])
                current_values[key] = val

            current_values[new_key] = new_val
            cookie_string = '; '.join(f'{key}={value}' for key, value in current_values.items())
            self.headers[cookie] = cookie_string

    def request_handler(self, method, url, *args, attempt=0, **kwargs):
        '''make an http request'''
        try:
            request = Request(self.parser.add_scheme(url), kwargs['data'], self.headers)
        except ValueError as e:
            self.logger.log(2, self.NAME, e, url)
            return None

        try:
            with closing(urlopen(request, timeout=20)) as response:
                if kwargs['store_cookies']:
                    self.cookie_jar.extract_cookies(response, request)
                return method(response, url, *args, attempt=attempt, **kwargs)
        except HTTPError as e:
            if e.code in (500, 502, 503, 504):
                # NOTE: servers sometimes return 50X when requesting large files, retrying usually works.
                kwargs['error'] = e
                return self.retry(method, url, *args, attempt=attempt, **kwargs)
            self.logger.log(2, self.NAME, e, url)
        except (RemoteDisconnected, timeout, URLError) as e:
            # QUESTION: should we really retry on url error?
            kwargs['error'] = e
            return self.retry(method, url, *args, attempt=attempt, **kwargs)
        except Exception as e:
            # NOTE: too many other possible exceptions to catch individually -> use catchall
            self.logger.log(2, self.NAME, e, url)

    def get(self, url, store_cookies=False):
        '''make a get request'''
        response = self.request_handler(self.ParsedResponse, url, data=None, store_cookies=store_cookies)
        if not response:
            return self.ParsedResponse(None)
        return response

    def post(self, url, data, store_cookies=False):
        '''make a post request'''
        if isinstance(data, dict):
            data = urlencode(data)

        response = self.request_handler(self.ParsedResponse, url, data=data.encode(), store_cookies=store_cookies)
        if not response:
            return self.ParsedResponse(None)
        return response

    def download(self, url, filepath):
        '''downloader front end'''
        return self.request_handler(self.downloader, url, filepath, data=None, store_cookies=False)

    def retry(self, method, url, *args, **kwargs):
        '''retry http operation'''
        kwargs['attempt'] += 1
        if kwargs['attempt'] > 5:
            self.logger.log(2, self.NAME, kwargs['error'], f'aborting after 5 attempts: {url}')
            return None

        self.logger.log(2, self.NAME, kwargs['error'], f'retry attempt {kwargs["attempt"]}: {url}')
        self.delay(kwargs['attempt'])

        return self.request_handler(method, url, *args, **kwargs)

    ####################################################################
    # io
    ####################################################################

    def downloader(self, response, url, filepath, *args, error='', **kwargs):
        '''download web content'''
        # NOTE: default buffer == 8192
        ext = self.parser.extension(url)
        filename = self.parser.extract_filename(filepath, self.args['slugify'])
        length = int(response.info().get('Content-Length', -1))
        read = 0

        if length >= 0 and length < self.MIN_SIZE:
            self.logger.log(2, self.NAME, 'skipping small file', f'{filename}{ext}')
            return None

        filepath = self.check_ext(filepath, response.info().get('Content-Type'))
        if os.path.exists(filepath):
            if kwargs['attempt'] > 0:
                # NOTE: remove files that timed out during initial read
                # WARNING: possible to erroneously remove legit files with same filename
                # FIXME: lazy approach
                os.remove(filepath)
            elif not self.args['force']:
                self.logger.log(2, self.NAME, 'file exists', f'{filename}{ext}')
                return None

        if response.info().get('Content-Encoding') == 'gzip':
            response = GzipFile(fileobj=BufferedReader(response))

        with open(filepath, 'wb') as file:
            while True:
                chunk = response.read(DEFAULT_BUFFER_SIZE)
                if not chunk:
                    break
                read += len(chunk)
                file.write(chunk)

        if length >= 0 and read < length:
            # TODO: add seek?
            # NOTE: add to headers:
            # Range: bytes=StartPos-
            os.remove(filepath)
            return self.retry(self.downloader, url, filepath, *args,
                              error='incomplete read', **kwargs)

        return True

    def write_file(self, content, path, iter=False):
        '''write to a text file'''
        # QUESTION: is this used? keep?
        try:
            with open(path, 'w') as file:
                if iter:
                    file.write('\n'.join(content))
                else:
                    file.write(content)
        except OSError as e:
            self.logger.log(2, self.NAME, e, path)

    def read_file(self, path, iter=False):
        '''read from a text file'''
        try:
            with open(path, 'r') as file:
                if iter:
                    return file.read().splitlines()
                else:
                    return file.read()
        except OSError as e:
            self.logger.log(2, self.NAME, e, path)

    ####################################################################
    # main url/file handling
    ####################################################################

    def check_ext(self, filepath, mimetype):
        '''compare guessed extension to header content type and change if necessary'''
        if mimetype and '/' in mimetype and 'octet-stream' not in mimetype:
            header_ext = f'.{mimetype.split(";")[0].split("/")[1]}'.replace('svg+xml', 'svg')
            guessed_ext = self.parser.extension(filepath)

            if guessed_ext and guessed_ext != header_ext:
                filepath = filepath.replace(guessed_ext, header_ext)
            elif not guessed_ext:
                # BUG: can cause multiple extensions in some cases
                filepath += header_ext

        return filepath

    def collect(self, url, filename='', clean=False):
        '''finalize and add urls to the collection'''
        if self.parser.filter(url):
            # FIXME: adding valid url check here rejects relative urls
            return None

        if clean:
            url = self.parser.sanitize(url)
        if self.args['filename']:
            filename = self.args['filename']
        elif not filename:
            filename = self.parser.extract_filename(url, self.args['slugify'])
        ext = self.parser.extension(url)

        # NOTE: add url and filename to collection as hashable string
        if isinstance(self.collection, list):
            self.collection.append(f'{self.parser.finalize(url)}-break-{filename}{ext}')
        else:
            self.collection.add(f'{self.parser.finalize(url)}-break-{filename}{ext}')

    def loot(self, save_loc=None, timeout=0):
        '''retrieve resources from collected urls'''
        looted, failed, file = 0, 0, 1
        timed_out = False
        if not save_loc:
            save_loc = self.path_main

        for item in self.collection:
            self.logger.progress(self.NAME, 'looting', file, len(self.collection))

            if timeout and failed >= timeout:
                timed_out = True
                break

            url, filename = item.split('-break-')

            if self.args['nodl']:
                print(url, end='\n\n')
                continue

            # ext = self.parser.extension(url)
            filepath = os.path.join(save_loc, filename)
            if os.path.exists(filepath):
                if self.args['noskip'] or self.args['filename']:
                    filepath = self.parser.make_unique(filepath)
                elif not self.args['force']:
                    self.logger.log(2, self.NAME, 'file exists', filename)
                    continue

            attempt = self.download(url, filepath)
            # FIXME: sites that always return data, such as html instead of 404 make iterator goblin run forever.
            if attempt:
                self.logger.log(2, self.NAME, 'success', filename)
                failed = 0
                looted += 1
            else:
                failed += 1

            file += 1
            self.delay()

        if self.args['nodl']:
            self.logger.log(1, self.NAME, 'info', f'{len(self.collection)} urls(s) collected', clear=True)
        else:
            self.logger.log(1, self.NAME, 'complete', f'{looted} file(s) looted', clear=True)

        return timed_out
