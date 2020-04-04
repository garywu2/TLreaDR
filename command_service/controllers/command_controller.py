from flask import request
from flask_restplus import Resource
from command_service.models.event import Event
from flask_restplus import fields
from command_service.api.restplus import api
from command_service.controllers.util import *

ns = api.namespace('events', description='Operations related to event command routes')

event_model = api.model('Event', {
    "event_uuid": fields.String(description='event uuid'),
})

@ns.route('/<string:event_uuid>')
class PostItem(Resource):
    @ns.expect(event_model, validate=False)
    def get(self, event_uuid):
        event = Event.query.filter_by(event_uuid=event_uuid).first()
        if event.event_blob['type'] == 'category':
            if event.event_blob['operation'] == 'add':
                return constructCategory(event.event_blob)
            if event.event_blob['operation'] == 'delete':
                remove_category = event.event_blob['category']
                return removeCategory(remove_category)

        if event.event_blob['type'] == 'user':
            if event.event_blob['operation'] == 'add':
                return constructUser(event.event_blob)
            if event.event_blob['operation'] == 'update':
                update_user_id = event.event_blob['id']
                return updateUser(update_user_id, event.event_blob)
            if event.event_blob['operation'] == 'delete':
                delete_user_id = event.event_blob['id']
                return removeUser(delete_user_id)

        if event.event_blob['type'] == 'comment':
            if event.event_blob['operation'] == 'add':
                return constructComment(event.event_blob)
            if event.event_blob['operation'] == 'update':
                update_comment_id = event.event_blob['id']
                return updateComment(update_comment_id, event.event_blob)
            if event.event_blob['operation'] == 'delete':
                delete_comment_id = event.event_blob['id']
                return removeComment(delete_comment_id)

        if event.event_blob['type'] == 'post':
            if event.event_blob['operation'] == 'add':
                add_post_category = event.event_blob['category']
                return constructPost(add_post_category, event.event_blob)
            if event.event_blob['operation'] == 'update':
                update_post_category = event.event_blob['category']
                update_post_id = event.event_blob['id']
                return updatePost(update_post_category, update_post_id, event.event_blob)
            if event.event_blob['operation'] == 'delete':
                delete_post_category = event.event_blob['category']
                delete_post_id = event.event_blob['id']
                return removePost(delete_post_category, delete_post_id)

        if event.event_blob['type'] == 'vote':
            if event.event_blob['operation'] == 'add':
                add_vote_category = event.event_blob['category']
                add_vote_id = event.event_blob['id']
                return constructVote(add_vote_category, add_vote_id, event.event_blob)
            if event.event_blob['operation'] == 'update':
                update_vote_category = event.event_blob['category']
                update_vote_id = event.event_blob['id']
                return updateVote(update_vote_category, update_vote_id, event.event_blob)
            if event.event_blob['operation'] == 'delete':
                delete_vote_category = event.event_blob['category']
                delete_vote_id = event.event_blob['id']
                return removeVote(delete_vote_category, delete_vote_id, event.event_blob)

        return "Failed to execute request", 500
