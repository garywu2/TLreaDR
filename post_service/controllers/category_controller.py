from flask_restplus import Resource, marshal
from datetime import datetime

from post_service.api.models import category_dto
from post_service.api.restplus import api
from post_service.models import db
from post_service.models.category import Category
from post_service.models.post import Post
from post_service.parsers.category_parsers import category_parser

ns = api.namespace('categories', description='Operations related to categories')


def date_converter(o):
    if isinstance(o, datetime):
        return o.__str__()


@ns.route('')
class CategoryCollection(Resource):
    @ns.marshal_list_with(category_dto)
    def get(self):
        """
        Gets all categories
        """
        results = Category.query.all()
        return results, 200

    @api.expect(category_parser)
    def post(self):
        """
        Adds a new category
        """
        args = category_parser.parse_args()

        try:
            new_category = Category(args['name'])
            db.session.add(new_category)
            db.session.commit()

        except Exception as e:
            return {"message": str(e)}, 500

        return marshal(new_category, category_dto), 200


@ns.route('/<string:category>')
class CategoryItem(Resource):
    @ns.response(code=201, model=category_dto, description='Success')
    @ns.response(code=404, description='Not Found')
    def get(self, category):
        """
        Gets a specified category
        """
        try:
            queried_category = Category.query.filter_by(name=category).first()
            if queried_category:
                return marshal(queried_category, category_dto), 200
            else:
                return {"message": 'category not found'}, 404

        except Exception as e:
            return {"message": str(e)}, 500

    @ns.expect(category_parser)
    def delete(self, category):
        """
        Deletes a category
        """
        try:
            category_to_be_deleted = Category.query.filter_by(name=category).first()

            if category_to_be_deleted:
                posts_in_category_to_be_deleted = Post.query.filter_by(category_uuid=category_to_be_deleted.category_uuid).all()

                for post in posts_in_category_to_be_deleted:
                    db.session.delete(post)

                db.session.delete(category_to_be_deleted)
                db.session.commit()

            else:
                return {'message': 'category not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'category has been deleted successfully.'}, 201
