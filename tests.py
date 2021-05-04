from collections import defaultdict
from assertpy import assert_that
import posts

class MockRetriever:
    def __init__(self, data):
        self._posts = defaultdict(lambda: [])
        _posts = (self.__post(*d) for d in data)
        for p in _posts:
            for tag in p['tags']:
                self._posts[tag].append(p)

    @staticmethod
    def __post(id, tags=['tech'], read=10):
        return {'id': id, 'tags': tags if isinstance(tags, list) else [tags], 'read': read}

    def posts(self, tag):
        return self._posts[tag]


def test_mock_sanity(mockretriever):
    result = mockretriever.posts('sanity')
    assert_that(result).is_length(1)
    assert_that(result[0]).is_equal_to({'id': 100, 'tags': ['sanity'], 'read': 100})
    result = mockretriever.posts('history')
    assert_that(result).is_length(3)
    print('WE\'RE SANE IT SEEMS!')
def test_basic():
    result = posts.get_posts(['sanity'])
    assert_that(result[0]).is_equal_to({'id': 100, 'tags': ['sanity'], 'read': 100})
    print('BASIC PASSED - handler\'s being tested')

def test_asc():
    result = posts.get_posts(['tech'])
    assert_that(result).is_length(4)
    for i in range(len(result) - 1):
        assert_that(result[i]['id']).is_less_than_or_equal_to(result[i+1]['id'])
    print('ASCENDING SORT WORKS')
def test_desc():
    result = posts.get_posts(['tech'], ascending=False)
    assert_that(result).is_length(4)
    for i in range(len(result) - 1):
        assert_that(result[i]['id']).is_greater_than_or_equal_to(result[i+1]['id'])
    print('DESCENDING SORT WORKS')

def test_sortfield():
    sortfield = 'read'
    result = posts.get_posts(['tech'], sortfield=sortfield)
    assert_that(result).is_length(4)
    for i in range(len(result) - 1):
        assert_that(result[i]['id']).is_less_than_or_equal_to(result[i+1][sortfield])
    print('SORTBY WORKS')

def test_twotags():
    techresults = posts.get_posts(['tech'])
    disjointresults = posts.get_posts(['sanity'])
    bothresults = posts.get_posts(['tech', 'sanity'])
    assert_that(bothresults).is_length(len(techresults) + len(disjointresults))
    print('TWO TAG RETRIEVAL WORKS')

def test_uniqueness():
    results = posts.get_posts(['tech', 'history'])
    ids = [post['id'] for post in results]
    # sets have no duplicate elements
    assert_that(ids).is_length(len(set(ids)))
    print('UNIQUENESS WORKS')

def unit():
    mockposts = [(0, 'tech'), (1, 'history'), (2, 'tech'), (10, ['history', 'tech']), (5, ['history', 'tech'], 5), (100, 'sanity', 100)]
    mockretriever = MockRetriever(mockposts)
    posts.handler.retriever = mockretriever
    test_mock_sanity(mockretriever)
    test_asc()
    test_desc()
    test_sortfield()
    test_twotags()
    test_uniqueness()

def functional():
    pass

def test():
    unit()
    functional()

if __name__ == '__main__':
    test()
