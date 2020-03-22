from flask_restplus import Resource, fields, reqparse, marshal

from server.api.restplus import api
from server.models import db
from server.models.comment import Comment

ns = api.namespace('comments', description='Operations related to comments')

comment_dto = api.model('comment', {
    'comment_uuid': fields.String(required=True, description='comment uuid'),
    'id': fields.Integer(required=True, description='comment id'),
    'comment_text': fields.String(required=True, description='comment text'),
    'comment_upvotes': fields.String(required=True, description='comment upvotes'),
    'comment_downvotes': fields.String(required=True, description='comment downvotes'),
    'author_uuid': fields.String(required=True, description='author uuid'),
    'post_uuid': fields.String(required=True, description='post uuid'),
    'path': fields.String(required=True, description='comment path'),
    'parent_id': fields.Integer(required=True, description='comment parent id')
})
comment_dto['nested_comment'] = fields.List(fields.Nested(comment_dto))

comment_parser = reqparse.RequestParser()
comment_parser.add_argument('text', required=True, type=str, help='comment text', location='json')
comment_parser.add_argument('author_uuid', required=True, type=str, help='comment author uuid', location='json')
comment_parser.add_argument('post_uuid', required=True, type=str, help='comment post uuid', location='json')
comment_parser.add_argument('parent_id', type=str, help='comment parent id', location='json')

def display_comment(comment):
    comment.nested_comment = comment.replies.all()

    for reply in comment.nested_comment:
        display_comment(reply)

@ns.route('/')
class CommentCollection(Resource):
    @ns.marshal_list_with(comment_dto)
    def get(self):
        """
        Gets all comments
        """
        try:
            comments = Comment.query.filter_by(parent_id=None).order_by(Comment.path).all()
            for comment in comments:
                display_comment(comment)
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
            new_comment.save()
            new_comment.make_path()
            new_comment.save()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'comment has been created successfully.'}, 201
