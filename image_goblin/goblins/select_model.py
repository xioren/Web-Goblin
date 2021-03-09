from meta import MetaGoblin


# NOTE: may work for modellink too --> investigate


class SelectGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'select goblin'
    ID = 'select'
    # NOTE: old
    API_URL = 'https://cms.selectmodel.com/api/graphql.php'
    # API_URL = 'https://cms-select.patr.onl/api/graphql.php'
    # SITE_IDS = {'atlanta': '6',
    #             'chicago': '7',
    #             'london': '9',
    #             'los-angeles': '8',
    #             'miami': '5',
    #             'milano': '4',
    #             'model': 'null',
    #             'paris': '3',
    #             'stockholm': '2'}

    def __init__(self, args):
        super().__init__(args)

    def extract_location(self, url):
        '''extract location from url'''
        return url.replace('https://', '').split('/')[1]

    def extract_model(self, url):
        '''extract model name from url'''
        return url.rstrip('/').split('/')[-1]

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'gallery' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'looting', target)
                self.logger.spin()

                model = self.extract_model(target)
                location = self.extract_location(target)
                # site_id = self.SITE_IDS[location]
                # model_id = self.parser.regex_search(r'(?<=gallery/)\d+|(?<=hero_image_file/)\d+', self.get(target).content)

                # query = {"query":"{solarnetModel(modelId: "+model_id+", siteSolarnetId: "+site_id+", site: \""+location+"\") { \n        id,\n        firstName,\n        lastName,\n        gender,\n        departmentId,\n        name,\n        slug,\n        bio,\n        image { url },\n        videos { url, type, image { url } },\n        heroImage { sizes { name, url }, orientation, file_dimensions_x, file_dimensions_y },\n        portfolio { url, orientation },\n        polaroids { url },\n        runways { url },\n        covers { url },\n        campaigns { url },\n        books { name, slug, images { url } },\n        measurements { label, value, humanValue, metric, imperial, ukSize },\n        instagram,\n        inTown,\n        uiControls,\n        uiLogoControls,\n        seo { \n        title,\n        description,\n        openGraphTitle,\n        openGraphDescription,\n        openGraphImage,\n        twitterTitle,\n        twitterDescription\n       }\n       }}"}

                query = self.parser.make_json({"operationName":"MODEL_QUERY","variables":{"modelUri":f"{model}","site":f"{location}"},"query":"query MODEL_QUERY($modelUri: String, $site: String) {\n  model(modelUri: $modelUri, site: $site) {\n    id\n    gender\n    firstName\n    lastName\n    slug\n    inTown\n    uiColour\n    uiLogoColour\n    bio\n    image {\n      ... on Image {\n        sourceUrl\n        __typename\n      }\n      __typename\n    }\n    heroImage {\n      ... on Image {\n        sourceUrl\n        width\n        height\n        __typename\n      }\n      __typename\n    }\n    heroImageDesktop {\n      ... on Image {\n        sourceUrl\n        width\n        height\n        __typename\n      }\n      __typename\n    }\n    portfolio {\n      ... on Image {\n        sourceUrl\n        orientation\n        __typename\n      }\n      __typename\n    }\n    polaroids {\n      ... on Image {\n        sourceUrl\n        __typename\n      }\n      __typename\n    }\n    runways {\n      ... on Image {\n        sourceUrl\n        __typename\n      }\n      __typename\n    }\n    covers {\n      ... on Image {\n        sourceUrl\n        __typename\n      }\n      __typename\n    }\n    campaigns {\n      ... on Image {\n        sourceUrl\n        __typename\n      }\n      __typename\n    }\n    videos {\n      ... on Video {\n        sourceUrl\n        videoType\n        __typename\n      }\n      __typename\n    }\n    books {\n      name\n      slug\n      assets {\n        ... on Image {\n          sourceUrl\n          __typename\n        }\n        ... on Video {\n          sourceUrl\n          videoType\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    measurements {\n      fieldName\n      fieldValue\n      fieldValueHuman {\n        us\n        metric\n        uk\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"})

                response = self.parser.load_json(self.post(self.API_URL, data=query).content)

                if 'data' in response:
                    for image in response['data']['model'].get('portfolio', ''):
                        urls.append(image.get('sourceUrl', ''))

                    for image in response['data']['model'].get('polaroids', ''):
                        urls.append(image.get('sourceUrl', ''))

                    for video in response['data']['model'].get('videos', ''):
                        urls.append(video.get('sourceUrl', ''))

            self.delay()

        for url in urls:
            self.collect(url.replace('expanded_medium/', ''))

        self.loot()
