import requests
from flask import request
import datetime
import time

from command_service.models.event import Event

startup_time = datetime.datetime.now()

# User events
def constructUser():
    response = requests.post('http://user_service:7082/api/users', json=request.json)
    return response.json(), response.status_code

def updateUser(uuid):
    response = requests.put('http://user_service:7082/api/users/' + uuid, json=request.json)
    return response.json(), response.status_code

def removeUser(uuid):
    response = requests.delete('http://user_service:7082/api/users/' + uuid)
    return response.json(), response.status_code

# Comment events
def constructComment():
    response = requests.post('http://comment_service:7082/api/comments', json=request.json)
    return response.json(), response.status_code

def updateComment(comment_uuid):
    response = requests.put('http://comment_service:7082/api/comments/' + comment_uuid, json=request.json)
    return response.json(), response.status_code

def removeComment(comment_uuid):
    response = requests.delete('http://comment_service:7082/api/comments/' + comment_uuid)
    return response.json(), response.status_code

# Post events
def constructPost(category):
    response = requests.post('http://post_service:7082/api/' + category + '/posts', json=request.json)
    return response.json(), response.status_code

def updatePost(category, post_uuid):
    response = requests.put('http://post_service:7082/api/' + category + '/' + post_uuid, json=request.json)
    return response.json(), response.status_code

def removePost(category, post_uuid):
    response = requests.delete('http://post_service:7082/api/' + category + '/' + post_uuid)
    return response.json(), response.status_code

# Vote events
def constructVote(category, post_uuid):
    response = requests.post('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
                             json=request.json)
    return response.json(), response.status_code

def updateVote(category, post_uuid):
    response = requests.put('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
                            json=request.json)
    return response.json(), response.status_code

def removeVote(category, post_uuid):
    response = requests.delete('http://post_service:7082/api/' + category + '/' + post_uuid + '/vote',
                               json=request.json)
    return response.json(), response.status_code

# Category events
def constructCategory():
    response = requests.post('http://post_service:7082/api/categories', json=request.json)
    return response.json(), response.status_code

def removeCategory(category):
    response = requests.delete('http://post_service:7082/api/categories/' + category)
    return response.json(), response.status_code

checked_time = startup_time
while True:
    time.sleep(2)
    new_events = Event.query.filter_by(Event.event_blob['time'].astext.cast(datetime) > checked_time).all()
    for event in new_events:

        if event.event_blob['type'] == 'category':
            if event.event_blob['operation'] == 'add':
                constructCategory()
            elif event.event_blob['operation'] == 'delete':
                removeCategory(event.event_blob['category'])

        elif event.event_blob['type'] == 'user':
            if event.event_blob['operation'] == 'add':
                constructUser()
            elif event.event_blob['operation'] == 'update':
                updateUser(event.event_blob['id'])
            elif event.event_blob['operation'] == 'delete':
                removeUser(event.event_blob['id'])

        elif event.event_blob['type'] == 'comment':
            if event.event_blob['operation'] == 'add':
                constructComment()
            elif event.event_blob['operation'] == 'update':
                updateComment(event.event_blob['id'])
            elif event.event_blob['operation'] == 'delete':
                removeComment(event.event_blob['id'])

        elif event.event_blob['type'] == 'post':
            if event.event_blob['operation'] == 'add':
                constructPost(event.event_blob['category'])
            elif event.event_blob['operation'] == 'update':
                updatePost(event.event_blob['category'], event.event_blob['id'])
            elif event.event_blob['operation'] == 'delete':
                removePost(event.event_blob['category'], event.event_blob['id'])

        elif event.event_blob['type'] == 'vote':
            if event.event_blob['operation'] == 'add':
                constructVote(event.event_blob['category'], event.event_blob['id'])
            elif event.event_blob['operation'] == 'update':
                updateVote(event.event_blob['category'], event.event_blob['id'])
            elif event.event_blob['operation'] == 'delete':
                removePost(event.event_blob['category'], event.event_blob['id'])

    checked_time = datetime.datetime.now()
