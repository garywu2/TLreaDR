from datetime import datetime

from flask_restplus import Resource, fields, reqparse

from server.api.restplus import api
from server.models import db
from server.models.comment import Comment

ns = api.namespace('comments', description='Operations related to comments')


def recursive_comment_mapping(level):
    comment_dto = {
        'comment_uuid': fields.String(required=True, description='comment uuid'),
        'id': fields.Integer(required=True, description='comment id'),
        'comment_text': fields.String(required=True, description='comment text'),
        'comment_upvotes': fields.String(required=True, description='comment upvotes'),
        'comment_downvotes': fields.String(required=True, description='comment downvotes'),
        'author_uuid': fields.String(required=True, description='author uuid'),
        'post_uuid': fields.String(required=True, description='post uuid'),
        'path': fields.String(required=True, description='comment path'),
        'parent_id': fields.Integer(required=True, description='comment parent id')
    }
    if level:
        comment_dto['nested_comment'] = fields.Nested(recursive_comment_mapping(level - 1))
    return api.model('Comment' + str(level), comment_dto)


comment_parser = reqparse.RequestParser()
comment_parser.add_argument('text', required=True, type=str, help='comment text', location='json')
comment_parser.add_argument('author_uuid', required=True, type=str, help='comment author uuid', location='json')
comment_parser.add_argument('post_uuid', required=True, type=str, help='comment post uuid', location='json')
comment_parser.add_argument('parent_id', type=str, help='comment parent id', location='json')

comment_edit_parser = reqparse.RequestParser()
comment_edit_parser.add_argument('new_text', required=True, type=str, help='new title of post', location='json')


def nest_comment(comment):
    comment.nested_comment = comment.replies.all()

    for reply in comment.nested_comment:
        nest_comment(reply)


@ns.route('/')
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

        return {'message': 'comment has been created successfully.'}, 201


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
            if comment_to_be_deleted:
                comment_to_be_deleted.is_deleted = True
                db.session.commit()
            else:
                return {'message': 'comment not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'comment has been deleted successfully.'}, 201


@ns.route('/<string:post_uuid>')
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
                .order_by(Comment.path).all()
            for comment in comments:
                nest_comment(comment)
            return comments
        except Exception as e:
            return {"message": str(e)}, 500