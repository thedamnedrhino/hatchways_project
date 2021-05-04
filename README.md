# Installation
This runs well on python 3.7
Run
>$ pip install -r requirements.txt

Then run

>$ FLASK_APP=app.py flask run

This will run your application at 127.0.0.1:5000 by default.

Go to `http://127.0.0.1:5000/api/ping` to test things out. 

# Overview
The code is shipped as a single package with no subpackages.  
It is a **Flask** application.  
The **app.py** file handles the HTTP API side of things (request/response parsing/generating) and relays the requests to the **posts** module.  
The **posts** module contains two classes: **PostsHandler** and **PostsRetriever**.  
**PostsHandler** takes care of the business logic, and **PostsRetriever** takes care of retrieving the posts from the external API. It has a cache sneaked in somewhere in there.

# Tests
To run the tests, first run the flask server as above.  
Then run
>$ python tests.py

The file contains **unit** and **functional** tests.  
The **unit** tests cover the business logic of **PostsHandler**, (e.g. uniqueness of posts, correct sorting), and the **functionals** cover well-formed request/responses on the API and make sure the params are communicated from the http request to the backend handler.

These are the two main functions:  

```

def unit():
    ...
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

```

