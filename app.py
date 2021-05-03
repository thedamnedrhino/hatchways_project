from flask import Flask, request, jsonify, make_response
import posts

app = Flask(__name__)

HTTP_SUCCESS=200

@app.route('/')
def hello_world():
    return 'Hello, World!, here is your passed parameters: {}'.format(request.args)

@app.route('/api/ping', methods=['GET'])
def ping():
    return make_response(jsonify({'success': True}), HTTP_SUCCESS)

@app.route('/api/posts', methods=['GET'])
def get_posts():
    requestdata, valid = validate_request(request)
    if not valid:
        return invalid_response(requestdata)
    posts = posts.get_posts(tags=requestdata['tags'], sortby=requestdata['sortby'], order=requestdata['direction'])
    return post_response(posts)

def validate_post_request(request):
    """request: the request object
    return: request_data|request_errors: dict, valid: bool"""
    pass
def invalid_response(validate_request_data):
    """validate_request_data: dict - returned from validate_post
    return: json response object"""
    pass

def post_response(posts):
    """posts: posts - from posts module
    return: json response object"""
    pass



