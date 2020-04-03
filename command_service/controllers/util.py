import requests

# User events
def constructUser(request_json):
    response = requests.post('http://user_service:7082/api/users', json=request_json)
    return response.json(), response.status_code

def updateUser(uuid, request_json):
    response = requests.put('http://user_service:7082/api/users/' + uuid, json=request_json)
    return response.json(), response.status_code

def removeUser(uuid):
    response = requests.delete('http://user_service:7082/api/users/' + uuid)
    return response.json(), response.status_code

# Comment events
def constructComment(request_json):
    response = requests.post('http://comment_service:7082/api/comments', json=request_json)
    return response.json(), response.status_code

def updateComment(comment_uuid, request_json):
    response = requests.put('http://comment_service:7082/api/comments/' + comment_uuid, json=request_json)
    return response.json(), response.status_code

def removeComment(comment_uuid):
    response = requests.delete('http://comment_service:7082/api/comments/' + comment_uuid)
    return response.json(), response.status_code

# Post events
def constructPost(category, request_json):
    response = requests.post('http://post_service:7082/api/' + category + '/posts', json=request_json)
    return response.json(), response.status_code

def updatePost(category, post_uuid, request_json):
    response = requests.put('http://post_service:7082/api/' + category + '/' + post_uuid, json=request_json)
    return response.json(), response.status_code

def removePost(category, post_uuid):
    response = requests.delete('http://post_service:7082/api/' + category + '/' + post_uuid)
    return response.json(), response.status_code

# Vote events
def constructVote(category, post_uuid, request_json):
    response = requests.post('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
                             json=request_json)
    return response.json(), response.status_code

def updateVote(category, post_uuid, request_json):
    response = requests.put('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
                            json=request_json)
    return response.json(), response.status_code

def removeVote(category, post_uuid, request_json):
    response = requests.delete('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
                               json=request_json)
    return response.json(), response.status_code

# Category events
def constructCategory(request_json):
    response = requests.post('http://post_service:7082/api/categories', json=request_json)
    return response.json(), response.status_code

def removeCategory(category):
    response = requests.delete('http://post_service:7082/api/categories/' + category)
    return response.json(), response.status_code
