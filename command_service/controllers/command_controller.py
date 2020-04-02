import requests
from flask import request
import datetime
import time
from flask_restplus import Resource
from command_service.models.event import Event
from flask_restplus import fields
from command_service.api.restplus import api

ns = api.namespace('events', description='Operations related to event command routes')

event_model = api.model('Event', {
    "event_uuid": fields.String(description='event uuid'),
})

def stripEvent(event_json):
    del event_json['time']
    del event_json['operation']
    del event_json['type']
    del event_json['category']
    del event_json['id']
    return event_json

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


@ns.route('/<string:event_uuid>')
class PostItem(Resource):
    @ns.expect(event_model, validate=False)
    def get(self, event_uuid):
        event = Event.query.filter_by(event_uuid=event_uuid).first()
        if event.event_blob['type'] == 'category':
            if event.event_blob['operation'] == 'add':
                event.event_blob = stripEvent(event.event_blob)
                return constructCategory(event.event_blob)
            elif event.event_blob['operation'] == 'delete':
                remove_category = event.event_blob['category']
                event.event_blob = stripEvent(event.event_blob)
                return removeCategory(remove_category)

        elif event.event_blob['type'] == 'user':
            if event.event_blob['operation'] == 'add':
                event.event_blob = stripEvent(event.event_blob)
                return constructUser(event.event_blob)
            elif event.event_blob['operation'] == 'update':
                update_user_id = event.event_blob['id']
                event.event_blob = stripEvent(event.event_blob)
                return updateUser(update_user_id, request.json)
            elif event.event_blob['operation'] == 'delete':
                delete_user_id = event.event_blob['id']
                event.event_blob = stripEvent(event.event_blob)
                return removeUser(delete_user_id)

        elif event.event_blob['type'] == 'comment':
            if event.event_blob['operation'] == 'add':
                event.event_blob = stripEvent(event.event_blob)
                return constructComment(event.event_blob)
            elif event.event_blob['operation'] == 'update':
                update_comment_id = event.event_blob['id']
                event.event_blob = stripEvent(event.event_blob)
                return updateComment(update_comment_id, event.event_blob)
            elif event.event_blob['operation'] == 'delete':
                delete_comment_id = event.event_blob['id']
                event.event_blob = stripEvent(event.event_blob)
                return removeComment(delete_comment_id)

        elif event.event_blob['type'] == 'post':
            if event.event_blob['operation'] == 'add':
                add_post_category = event.event_blob['category']
                event.event_blob = stripEvent(event.event_blob)
                return constructPost(add_post_category, event.event_blob)
            elif event.event_blob['operation'] == 'update':
                update_post_category = event.event_blob['category']
                update_post_id = event.event_blob['id']
                event.event_blob = stripEvent(event.event_blob)
                return updatePost(update_post_category, update_post_id, event.event_blob)
            elif event.event_blob['operation'] == 'delete':
                delete_post_category = event.event_blob['category']
                delete_post_id = event.event_blob['id']
                event.event_blob = stripEvent(event.event_blob)
                return removePost(delete_post_category, delete_post_id)

        elif event.event_blob['type'] == 'vote':
            if event.event_blob['operation'] == 'add':
                add_vote_category = event.event_blob['category']
                add_vote_id = event.event_blob['id']
                event.event_blob = stripEvent(event.event_blob)
                return constructVote(add_vote_category, add_vote_id, event.event_blob)
            elif event.event_blob['operation'] == 'update':
                update_vote_category = event.event_blob['category']
                update_vote_id = event.event_blob['id']
                event.event_blob = stripEvent(event.event_blob)
                return updateVote(update_vote_category, update_vote_id, event.event_blob)
            elif event.event_blob['operation'] == 'delete':
                delete_vote_category = event.event_blob['category']
                delete_vote_id = event.event_blob['id']
                event.event_blob = stripEvent(event.event_blob)
                return removePost(delete_vote_category, delete_vote_id)

        else:
            return "Failed to execute request", 500
