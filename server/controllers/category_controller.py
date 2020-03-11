from flask_restplus import Resource, fields, reqparse, marshal

from server.api.restplus import api
from server.models import db
from server.models.category import Category

ns = api.namespace('categories', description='Operations related to categories')

category_dto = api.model('category', {
    'category_uuid': fields.String(required=True, description='category uuid'),
    'name': fields.String(required=True, description='category name'),
})

category_parser = reqparse.RequestParser()
category_parser.add_argument('name', required=True, type=str, help='name of category', location='json')


@ns.route('')
class CategoryCollection(Resource):
    @ns.marshal_list_with(category_dto)
    def get(self):
        """
        Gets all categories
        """
        results = Category.query.all()
        return results

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

        return {'message': 'category has been created successfully.'}, 201


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
                return marshal(queried_category, category_dto)
            else:
                return {"message": 'category not found'}, 404

        except Exception as e:
            return {"message": str(e)}, 500

    @ns.expect(category_parser)
    def delete(self):
        """
        Deletes a user
        """
        args = category_parser.parse_args()

        category_to_be_deleted_name = args['name']

        try:
            category_to_be_deleted = Category.query.filter_by(name=category_to_be_deleted_name).first()
            if category_to_be_deleted:
                db.session.delete(category_to_be_deleted)
                db.session.commit()
            else:
                return {'message': 'category not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'category has been deleted successfully.'}, 201
