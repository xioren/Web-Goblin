from time import time
from json import dumps
from os.path import join
from getpass import getpass
from urllib.parse import quote, urljoin

from meta import MetaGoblin

# NOTE: pagination /?__a=1
# NOTE: ig_id

class InstagramGoblin(MetaGoblin):
    '''code inspired by:
        - https://github.com/rarcega/instagram-scraper
        - https://github.com/ytdl-org/youtube-dl
        - various stack overflow posts
    '''

    NAME = 'instagram goblin'
    ID = 'instagram'
    BASE_URL = 'https://www.instagram.com'
    LOGOUT_URL = BASE_URL + '/accounts/logout/ajax/'
    LOGIN_URL = BASE_URL + '/accounts/login/ajax/'
    SEARCH_URL = BASE_URL + '/web/search/topsearch/?query='
    # POST_URL = BASE_URL + '/graphql/query/?query_hash=1451128a3ce596b72f20c738dc7f0f73&variables={}'
    MEDIA_URL = BASE_URL + '/graphql/query/?query_hash=44efc15d3c13342d02df0b5a9fa3d33f&variables={}'
    # TAGGED_URL = BASE_URL + '/graphql/query/?query_hash=ff260833edf142911047af6024eb634a&variables={}'
    STORIES_IDS_URL = BASE_URL + '/graphql/query/?query_hash=d4d88dc1500312af6f937f7b804c68c&variables={}'
    STORIES_MEDIA_URL = BASE_URL + '/graphql/query/?query_hash=0a85e6ea60a4c99edc58ab2f3d17cfdf&variables={}'

    def __init__(self, args):
        super().__init__(args)
        self.logged_in = False
        self.num_posts = self.args['posts'] if self.args['posts'] < 100 else 100

    def setup(self, url):
        '''initialize user'''
        self.username = self.extract_username(url)
        self.user_dir = join(self.path_main, self.username)

        self.make_dirs(self.user_dir)

    def extract_username(self, url):
        if '/p/' in url:
            shortcode = url.rstrip('/').split('/')[-1]
            variables = f'{{"shortcode":"{shortcode}","include_reel":true}}'
            response = self.parser.load_json(self.get(self.POST_URL.format(quote(variables, safe='"'))).content)
            return response['data']['shortcode_media']['owner']['reel']['owner']['username']
        else:
            return url.rstrip('/').split('/')[-1]

    def authenticate(self, login):
        '''login to instagram or authenticate as guest'''
        # NOTE: csrf token doesnt seem necessary, at least while not logged in.
        response = self.get(self.BASE_URL, store_cookies=True)
        self.set_cookies()

        if login:
            # FIXME: currently does not work --> changes on instagrams side
            while True:
                username = input(f'[{self.NAME}] username: ')
                password = getpass(f'[{self.NAME}] password: ')
                formatted_password = f"#PWD_INSTAGRAM_BROWSER:0:{int(time())}:{password}"
                response = self.parser.load_json(self.post(self.LOGIN_URL,
                                                           data={'username': username,
                                                                 'enc_password': formatted_password},
                                                           store_cookies=True).content)
                self.set_cookies()
                del username, password

                if 'authenticated' in response:
                    self.logged_in = True
                    self.logger.log(0, self.NAME, 'logged in')
                elif 'checkpoint_url' in response:
                    self.logger.log(0, self.NAME, 'WARNING', 'account verification required')
                    self.verify_account(response['checkpoint_url'])
                else:
                    self.logger.log(0, self.NAME, 'ERROR', 'login failed')
                    retry = input(f'[{self.NAME}] retry? (y/n): ')
                    if retry in ('y', 'Y', 'yes', "YES"):
                        continue
                    self.logger.log(0, self.NAME, 'continuing as guest')
                break

    def logout(self):
        response = self.post(self.LOGOUT_URL, data={"one_tap_app_login": 0})

        if response.code == 200:
            self.logger.log(0, self.NAME, 'logged out')
        else:
            self.logger.log(0, self.NAME, 'ERROR', 'logout failed')

    def verify_account(self, checkpoint_url):
        '''complete security challenge to verify account'''
        # WARNING: untested
        verify_url = urljoin(self.BASE_URL, checkpoint_url)
        response = self.get(verify_url, store_cookies=True)
        self.set_cookies()

        self.headers.update(
            {
                'X-Instagram-AJAX': '1',
                'Referer': verify_url
            }
        )

        mode = input(f'[{self.NAME}] receive code via (0 - sms, 1 - email): ')
        challenge = self.post(verify_url, data= {'choice': mode}, store_cookies=True)
        self.set_cookies()

        while True:
            code = int(input(f'[{self.NAME}] enter security code: '))
            response = self.post(verify_url, data={'security_code': code}, store_cookies=True)
            self.set_cookies()
            answer = self.parser.load_json(response.content)

            if answer.get('status') == 'ok':
                self.logged_in = True
                self.logger.log(0, self.NAME, 'logged in')
            else:
                self.logger.log(0, self.NAME, 'ERROR', 'security challenge failed')
                retry = input(f'[{self.NAME}] retry? (y/n): ')
                if retry in ('y', 'Y', 'yes', "YES"):
                    continue
                self.logger.log(0, self.NAME, 'continuing as guest')
            break

    def get_initial_data(self):
        '''make initial request to recieve necessary variables'''
        # WARNING: deprecated
        self.extend_cookie('Cookie', 'ig_pr=1')
        response = self.get(urljoin(self.BASE_URL, self.username)).content
        if response:
            data = self.parser.load_json(self.parser.regex_search(r'(?<=sharedData\s=\s){.+?}(?=;)', response))

            if 'entry_data' in data:
                self.user_id = data['entry_data']['ProfilePage'][0]['graphql']['user']['id']
                self.rhx_gis = response.get('rhx_gis', '3c7ca9dcefcf966d11dacf1f151335e8')
                return True
        self.logger.log(2, self.NAME, 'ERROR', 'failed to get user id')
        return False

    def get_user_id(self):
        '''make initial request to obtain user id'''
        response = self.get(f'{self.SEARCH_URL}{self.username}')
        try:
            response = self.parser.load_json(response.content)
        except:
            response = ''

        if 'users' in response and response['users']:
            self.user_id = response['users'][0]['user']['pk']
            return True

        self.logger.log(2, self.NAME, 'ERROR', 'failed to get user id')
        return False

    def parse_profile(self):
        '''collect and parse instagram posts'''
        cursor = ''

        self.headers.update({'X-Requested-With': 'XMLHttpRequest'})

        self.logger.log(1, self.NAME, 'parsing profile', self.username)

        while True:
            variables = dumps(
                {
                    'id': self.user_id,
                    'first': self.num_posts,
                    'after': cursor
                }
            )

            response = self.parser.load_json(self.get(self.MEDIA_URL.format(quote(variables, safe='"'))).content)
            if 'data' in response:
                # NOTE: 'edge_user_to_photos_of_you' for tagged media
                for edge in response['data']['user']['edge_owner_to_timeline_media'].get('edges', ''):
                    self.extract_media(edge)
                    if 'edge_sidecar_to_children' in edge.get('node', ''): # post has multiple images/videos
                        for inner_edge in edge['node']['edge_sidecar_to_children'].get('edges', ''):
                            self.extract_media(inner_edge)

            cursor = response['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

            if not cursor or self.num_posts < 100:
                # end of profile or user specified finite number of posts.
                break

            self.delay()

    def extract_media(self, edge):
        '''extract media from json'''
        image_url = edge['node']['display_url']
        video_url = edge['node'].get('video_url')
        self.collect(image_url, f'{self.username}_{self.parser.extract_filename(image_url)}')
        if video_url:
            self.collect(video_url, f'{self.username}_{self.parser.extract_filename(video_url)}')

    def get_stories(self, url):
        '''extract media from stories'''
        response = self.parser.load_json(self.get(url).content)

        if 'data' in response:
            for reel_media in response['data'].get('reels_media', ''):
                for item in reel_media.get('items', ''):
                    url = item['display_url']
                    self.collect(url, f'{self.username}_{self.parser.extract_filename(url)}')

                    if 'video_resources' in item:
                        # NOTE: the last item in the list is the highest quality
                        url = item['video_resources'][-1]['src']
                        self.collect(url, f'{self.username}_{self.parser.extract_filename(url)}')

    def get_main_stories(self):
        '''get main instagram stories'''
        self.get_stories(self.STORIES_MEDIA_URL.format(quote('{{"reel_ids":["{}"],"tag_names":[],"location_ids":[],' \
                                                             '"highlight_reel_ids":[],"precomposed_overlay":false,' \
                                                             '"show_story_viewer_list":false,"stories_video_dash_manifest":false}}'.format(self.user_id), safe='"')))

    def get_highlight_stories(self):
        '''get highlight instagram stories'''
        # NOTE: get highlight reels ids
        response = self.parser.load_json(self.get(self.STORIES_IDS_URL.format(quote('{{"user_id":"{}","include_chaining":false,' \
                                                                                    '"include_reel":false,"include_suggested_users":false,' \
                                                                                    '"include_logged_out_extras":false,"include_highlight_reels":true,' \
                                                                                    '"include_live_status":true}}'.format(self.user_id), safe='"'))).content)

        if 'data' in response:
            higlight_reels_ids = [item['node']['id'] for item in response['data']['user']['edge_highlight_reels']['edges']]
            # NOTE: can only request 3 at a time --> get chunks of 3
            ids_chunks = [higlight_reels_ids[i:i + 3] for i in range(0, len(higlight_reels_ids), 3)]

            # NOTE: get media from reels
            for ids_chunk in ids_chunks:
                self.get_stories(self.STORIES_MEDIA_URL.format(quote('{{"reel_ids":[],"tag_names":[],"location_ids":[],' \
                                                                     '"highlight_reel_ids":["{}"],"precomposed_overlay":false,' \
                                                                     '"show_story_viewer_list":false,"stories_video_dash_manifest":false}}'.format('","'.join(str(x) for x in ids_chunk)), safe='"')))

    def main(self):
        self.authenticate(self.args['login'])

        for target in self.args['targets'][self.ID]:
            self.logger.log(2, self.NAME, 'looting', target)
            # self.logger.spin()

            if 'cdninstagram' in target:
                self.collect(target)
                self.loot()
            else:
                self.new_collection()
                self.setup(target)
                if '/p/' in target:
                    self.logger.log(0, self.NAME, 'ERROR', 'post urls are temporarily disabled')
                else:
                    if self.args['mode'] in ('latest', 'recent'):
                        self.num_posts = 6
                    retrieved_data = self.get_user_id()

                    if retrieved_data:
                        if self.logged_in:
                            self.logger.log(1, self.NAME, 'collecting stories')
                            self.get_main_stories()
                            if self.args['mode'] not in ('latest', 'recent'):
                                self.get_highlight_stories()

                        self.parse_profile()

                self.loot(save_loc=self.user_dir)
                self.move_vid(self.user_dir)
        if self.logged_in:
            self.logout()
