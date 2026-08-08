from ddgs import DDGS


class DDGSClient:
    def __init__(self):
        self.client = DDGS()

    def search_text(self, keyword: str):
        return self.client.text(keyword)

    def search_image(self, keyword: str):
        return self.client.images(keyword)

    def search_news(self, keyword: str):
        return self.client.news(keyword)

    def search_video(self, keyword: str):
        return self.client.videos(keyword)

if __name__ == '__main__':
    from pprint import pprint
    ddgsc = DDGSClient()
    keyword = 'Bethlehem'
    pprint(ddgsc.search_text(keyword))
    # pprint(ddgsc.search_image(keyword))
    # pprint(ddgsc.search_news(keyword))
    # pprint(ddgsc.search_video(keyword))
