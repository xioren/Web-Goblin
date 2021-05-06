from goblins.generic_alpha import AlphaGoblin


# NOTE: http://tienda.promise.es/


class PromiseGoblin(AlphaGoblin):

    NAME = 'promise goblin'
    ID = 'promise'
    ACCEPT_IMAGE = False
    ACCEPT_WEBPAGE = True

    def __init__(self, args):
        super().__init__(args)

    def generate_urls(self, url, image=True):
        if image:
            return [url]
        else:
            return self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)
