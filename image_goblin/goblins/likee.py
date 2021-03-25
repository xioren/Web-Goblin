from meta import MetaGoblin


class LikeeGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'likee goblin'
    ID = 'likee'
    API_URL = 'https://likee.com/official_website/VideoApi/getUserVideo'

    def __init__(self, args):
        super().__init__(args)
        self.num_posts = self.args['posts'] if self.args['posts'] < 100 else 100

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if '/s/' in target:
                response = self.get(target).content
                urls.append(self.parser.regex_search(r'(?<=video_url":")[^"]+', response))
                # urls.append(self.parser.regex_search(r'(?<=thumbnailUrl":\[")[^"]+', response))
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                last_postid = ''
                init_response = self.get(self.parser.dequery(target)).content
                uid = self.parser.regex_search(r'(?<="uid":")\d+', init_response)

                while True:
                    self.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
                    response = self.parser.from_json(self.post(self.API_URL, {'uid': uid, 'count': self.num_posts, 'lastPostId': last_postid}).content)
                    if response['msg'] == 'success':
                        if not response['data']['videoList']:
                            break
                        for post in response['data']['videoList']:
                            # urls.append(post['coverUrl'])
                            urls.append(post['videoUrl'])
                        last_postid = response['data']['videoList'][-1]['postId']
                    else:
                        # OPTIMIZE: two breaks, should be combined.
                        break

                    if self.num_posts < 100:
                        # end of profile or user specified finite number of posts.
                        break

                    self.delay()
        del self.headers['Content-Type']
        for url in urls:
            self.collect(url)

        self.loot()
