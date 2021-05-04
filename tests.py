from collections import defaultdict
import requests
from assertpy import assert_that
import posts

SERVER_ADDRESS = 'http://127.0.0.1:5000'

class MockRetriever:
    def __init__(self, data):
        self._posts = defaultdict(lambda: [])
        _posts = (self.__post(*d) for d in data)
        for p in _posts:
            for tag in p['tags']:
                self._posts[tag].append(p)

    @staticmethod
    def __post(id, tags=['tech'], reads=10):
        return {'id': id, 'tags': tags if isinstance(tags, list) else [tags], 'reads': reads}

    def posts(self, tag):
        return self._posts[tag]


def test_mock_sanity(mockretriever):
    result = mockretriever.posts('sanity')
    assert_that(result).is_length(1)
    assert_that(result[0]).is_equal_to({'id': 100, 'tags': ['sanity'], 'reads': 100})
    result = mockretriever.posts('history')
    assert_that(result).is_length(3)
    print('WE\'RE SANE IT SEEMS!')
def test_basic():
    result = posts.get_posts(['sanity'])
    assert_that(result[0]).is_equal_to({'id': 100, 'tags': ['sanity'], 'reads': 100})
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
    sortfield = 'reads'
    result = posts.get_posts(['tech'], sortfield=sortfield)
    assert_that(result).is_length(4)
    for i in range(len(result) - 1):
        assert_that(result[i]['id']).is_less_than_or_equal_to(result[i+1][sortfield])
    print('SORTBY WORKS')

def test_multipletags_disjoint():
    techresults = posts.get_posts(['tech'])
    disjointresults = posts.get_posts(['sanity'])
    bothresults = posts.get_posts(['tech', 'sanity'])
    assert_that(bothresults).is_length(len(techresults) + len(disjointresults))
    print('MULTIPLE TAG RETRIEVAL IS SANE!')

def test_multipletags_uniqueness():
    results = posts.get_posts(['tech', 'history'])
    ids = [post['id'] for post in results]
    # sets have no duplicate elements
    assert_that(ids).is_length(len(set(ids)))
    print('UNIQUENESS WORKS')


def request(endpoint, params):
    response = requests.get('{}/api/{}'.format(SERVER_ADDRESS, endpoint), params)
    return response.json(), response.status_code
def request_posts(tags, sortfield=None, direction=None):
    params = {'tags': tags}
    if not sortfield is None:
        params['sortBy'] = sortfield
    if not direction is None:
        params['direction'] = direction
    return request('posts', params)

def test_ping():
    json, stat = request('ping', {})
    assert_that(stat).is_equal_to(200)
    assert_that(json).is_equal_to({'success': True})
    print('PING WORKS')

def test_posts_sanity():
    json, stat = request_posts(['asdfasdf'])
    assert_that(stat).is_equal_to(200)
    assert_that(json).contains_key('posts')
    assert_that(json['posts']).is_length(0)
    json, stat = request_posts(['tech'])
    assert_that(stat).is_equal_to(200)
    assert_that(len(json['posts'])).is_greater_than(0)
    print('POSTS ARE SANE!')

def test_no_tag():
    json, stat = request_posts([])
    assert_that(stat).is_equal_to(400)
    assert_that(json).contains('error')
    assert_that(json['error']).contains('Tags')
    print('NO TAGS (shouldn\'t work and they) DON\'T WORK')

def test_bad_sortby():
    json, stat = request_posts(['tech'], sortfield='reads')
    assert_that(stat).is_equal_to(200)
    json, stat = request_posts(['tech'], sortfield='non_existent_field')
    assert_that(stat).is_equal_to(400)
    assert_that(json).contains('error')
    assert_that(json['error']).contains('sortBy')
    print('SORTBY PARAM IS BAD-INPUT-CHECKED')


def test_bad_direction():
    json, stat = request_posts(['tech'], direction='baddirection')
    assert_that(stat).is_equal_to(400)
    assert_that(json).contains('error')
    assert_that(json['error']).contains('direction')
    print('DIRECTION PARAM IS BAD-INPUT CHECKED')

def test_custom_sort():
    json, stat = request_posts(['tech'], sortfield='reads', direction='desc')
    assert_that(stat).is_equal_to(200)
    assert_that(json).contains('posts')
    for i in range(len(json['posts']) - 1):
        assert_that(json['posts'][i]['reads']).is_greater_than_or_equal_to(json['posts'][i+1]['reads'])
    print('SORT PARAMETERS (sortBy, direction) WORK (reach the backend)')


def unit():
    mockposts = [(0, 'tech'), (1, 'history'), (2, 'tech'), (10, ['history', 'tech']), (5, ['history', 'tech'], 5), (100, 'sanity', 100)]
    mockretriever = MockRetriever(mockposts)
    posts.handler.retriever = mockretriever
    test_mock_sanity(mockretriever)
    test_asc()
    test_desc()
    test_sortfield()
    test_multipletags_disjoint()
    test_multipletags_uniqueness()

def functional():
    test_ping()
    test_posts_sanity()
    test_no_tag()
    test_bad_sortby()
    test_bad_direction()
    test_custom_sort()

def test():
    print()
    print('Running unit tests with a mocked external api***********')
    print()
    unit()
    print()
    print()
    print('Now some functional tests that will check well formed request/response pairs and error conditions**********')
    print()
    functional()
    print()
    print('...')
    print()
    print('So you needed a kickass dev, huh?')
    print()
    print()

if __name__ == '__main__':
    test()
