from datetime import datetime

from flask_restplus import Resource, fields, marshal
from sqlalchemy import desc

from comment_service.api.restplus import api
from comment_service.models import db
from comment_service.models.comment import Comment
from comment_service.parsers.comment_parsers import *

ns = api.namespace('comments', description='Operations related to comments')


def recursive_comment_mapping(level):
    comment_dto = {
        'comment_uuid': fields.String(required=True, description='comment uuid'),
        'id': fields.Integer(required=True, description='comment id'),
        'comment_text': fields.String(required=True, description='comment text'),
        'comment_upvotes': fields.String(required=True, description='comment upvotes'),
        'comment_downvotes': fields.String(required=True, description='comment downvotes'),
        'date_submitted': fields.String(required=True, description='submission date'),
        'date_edited': fields.String(required=True, description='edit date'),
        'is_edited': fields.Boolean(required=True, description='true if comment has been edited'),
        'is_deleted': fields.Boolean(required=True, description='true if comment has been deleted'),
        'author_uuid': fields.String(required=True, description='author uuid'),
        'author_username': fields.String(required=True, description='author uuid'),
        'post_uuid': fields.String(required=True, description='post uuid'),
        'path': fields.String(required=True, description='comment path'),
        'parent_id': fields.Integer(required=True, description='comment parent id')
    }
    if level:
        comment_dto['nested_comment'] = fields.Nested(recursive_comment_mapping(level - 1))
    return api.model('Comment' + str(level), comment_dto)


def nest_comment(comment):
    comment.nested_comment = comment.replies.all()

    for reply in comment.nested_comment:
        nest_comment(reply)


@ns.route('')
class CommentCollection(Resource):
    @ns.marshal_list_with(recursive_comment_mapping(10))
    def get(self):
        """
        Gets all comments
        """
        try:
            comments = Comment.query.filter_by(parent_id=None).order_by(Comment.path).all()
            for comment in comments:
                nest_comment(comment)
            return comments
        except Exception as e:
            return {"message": str(e)}, 500

    @api.expect(comment_parser)
    def post(self):
        """
        Adds a new comment
        """
        args = comment_parser.parse_args()

        try:
            new_comment = Comment(args['text'], args['author_uuid'], args['post_uuid'], args['parent_id'])
            # First save is required to save the comment to the db and generate an auto-incremented id
            new_comment.save()
            # The id of the comment is then used to make the path of the comment
            new_comment.make_path()
            # The path changes are committed again to the db using a second save
            new_comment.save()
        except Exception as e:
            return {"message": str(e)}, 500

        return marshal(new_comment, recursive_comment_mapping(0)), 201


@ns.route('/<string:comment_uuid>')
class CommentItem(Resource):
    @ns.expect(comment_edit_parser)
    def put(self, comment_uuid):
        """
        Updates an existing comment
        """
        args = comment_edit_parser.parse_args()

        try:
            comment_to_be_edited = Comment.query.filter_by(comment_uuid=comment_uuid).first()

            if comment_to_be_edited:
                if args['new_text']:
                    comment_to_be_edited.comment_text = args['new_text']

                comment_to_be_edited.date_edited = datetime.utcnow()
                comment_to_be_edited.is_edited = True
            else:
                return {'message': 'comment specified not found in database'}, 201

            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'comment has been edited successfully.'}, 201

    def delete(self, comment_uuid):
        """
        Deletes a comment
        """
        try:
            comment_to_be_deleted = Comment.query.filter_by(comment_uuid=comment_uuid).first()
            deleted_text = "[deleted]"
            deleted_uuid = "00000000-00000000-00000000-00000000"
            if comment_to_be_deleted:
                comment_to_be_deleted.is_deleted = True
                comment_to_be_deleted.comment_text = deleted_text
                comment_to_be_deleted.author_username = deleted_text
                comment_to_be_deleted.author_uuid = deleted_uuid
                db.session.commit()
            else:
                return {'message': 'comment not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'comment has been deleted successfully.'}, 201


@ns.route('/post/<string:post_uuid>')
class PostComment(Resource):
    @ns.marshal_list_with(recursive_comment_mapping(10))
    def get(self, post_uuid):
        """
        Gets all comments for post specified
        """
        try:
            comments = Comment.query \
                .filter_by(parent_id=None) \
                .filter_by(post_uuid=post_uuid) \
                .order_by(desc(Comment.date_submitted)).all()

            for comment in comments:
                nest_comment(comment)

            return comments
        except Exception as e:
            return {"message": str(e)}, 500

    def delete(self, post_uuid):
        """
        Deletes all comments for post specified
        """
        try:
            comments_to_be_deleted = Comment.query.filter_by(post_uuid=post_uuid).all()

            for comment in comments_to_be_deleted:
                db.session.delete(comment)
                db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'comments for post has been deleted successfully.'}, 200


@ns.route('/user/<string:user_uuid>')
class UserComments(Resource):
    @ns.marshal_list_with(recursive_comment_mapping(0))
    def get(self, user_uuid):
        """
        Gets all comments for user specified
        """
        try:
            comments = Comment.query \
                .filter_by(author_uuid=user_uuid) \
                .order_by(desc(Comment.date_submitted)).all()

            return comments
        except Exception as e:
            return {"message": str(e)}, 500

@ns.route('/<string:comment_uuid>/vote')
class CommentVote(Resource):
    @ns.expect(comment_vote_add_parser)
    def post(self, category, comment_uuid):
        """
        Creates a comment vote record
        """
        args = comment_vote_add_parser.parse_args()
        try:
            new_comment_vote = CommentVote(comment_uuid, args['user_uuid'], args['vote_type'])
            comment_voted_on = Comment.query.filter_by(comment_uuid=comment_uuid).first()
            comment_voted_on.assign_vote(args['vote_type'])
            db.session.add(new_comment_vote)
            db.session.commit()
            return {'message': 'vote has been created successfully.'}, 201
        except Exception as e:
            return {"message": str(e)}, 500

    @ns.expect(comment_vote_edit_parser)
    def put(self, comment_uuid, category):
        """
        Updates a vote record
        """
        args = comment_vote_edit_parser.parse_args()
        try:
            user_uuid = args['user_uuid']
            new_vote_type = args['new_vote_type']
            comment_to_be_edited = Comment.query.filter_by(comment_uuid=comment_uuid).first()
            vote_to_be_edited = CommentVote.query.filter_by(comment_uuid=comment_uuid) \
                .filter_by(user_uuid=user_uuid).first()

            if vote_to_be_edited and comment_to_be_edited:
                if vote_to_be_edited.vote_type == new_vote_type:
                    return {'message': 'cannot vote twice on the same comment'}, 404
                vote_to_be_edited.vote_type = new_vote_type
                comment_to_be_edited.assign_vote(2 * new_vote_type)
                db.session.add(comment_to_be_edited)
                db.session.commit()
                return {'message': 'vote has been edited successfully.'}, 201
            return {'message': 'vote or comment not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

    @ns.expect(comment_vote_delete_parser)
    def delete(self, comment_uuid, category):
        """
        Deletes a vote
        """
        args = comment_vote_delete_parser.parse_args()
        try:
            user_uuid = args['user_uuid']
            comment_to_be_edited = Comment.query.filter_by(comment_uuid=comment_uuid).first()
            vote_to_be_deleted = CommentVote.query.filter_by(comment_uuid=comment_uuid) \
                .filter_by(user_uuid=user_uuid).first()
            comment_to_be_edited.delete_vote(vote_to_be_deleted.vote_type)
            db.session.delete(vote_to_be_deleted)
            db.session.commit()
            return {'message': 'vote has been deleted successfully.'}, 201
        except Exception as e:
            return {"message": str(e)}, 500