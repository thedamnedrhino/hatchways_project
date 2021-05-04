import requests, requests_cache
import config

class PostHandler:
    def __init__(self, retriever):
        self.retriever = retriever

    def get_posts(self, tags, sortfield, ascending):
        posts = {}
        for tag in tags:
            posts.update({post['id']: post for post in self.retriever.posts(tag)})
        return sorted(posts.values(), reverse=(not ascending), key=lambda post: post[sortfield])


class PostRetriever:
    def __init__(self, url):
        self.url = url

    def posts(self, tag):
        return requests.get(self.url, params={'tag': tag}).json()['posts']


retriever = PostRetriever(config.POST_API_URL)
handler = PostHandler(retriever)

if config.CACHE:
    requests_cache.install_cache('posts', backend='sqlite', expire_after=180)

def get_posts(tags, sortfield='id', ascending=True):
    return handler.get_posts(tags, sortfield, ascending)
