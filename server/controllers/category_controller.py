from flask_restplus import Resource, fields, reqparse
from flask import request, make_response

from server.api.restplus import api
from server.models.category import Category
from server.models import db

ns = api.namespace('categories', description='Operations related to categories')

category_dto = api.model('category', {
    'category_uuid': fields.String(required=True, description='category uuid'),
    'name': fields.String(required=True, description='category name'),
})

category_parser = reqparse.RequestParser()
category_parser.add_argument('name', required=True, type=str, help='name of category')

@ns.route('/')
class CategoryList(Resource):
    @ns.marshal_list_with(category_dto)
    def get(self):
        """
        Gets all categories
        """
        results = Category.query.all()
        return results


@ns.route('/add')
class AddCategory(Resource):

    @api.expect(category_parser)
    def post(self):
        """
        Adds a new category
        """
        data = request.args

        try:
            newCategory = Category(data.get('name'))
            db.session.add(newCategory)
            db.session.commit()
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'category has been created successfully.'}, 201


@ns.route('/delete')
class DeleteCategory(Resource):

    @ns.expect(category_parser)
    def delete(self):
        """
        Deletes a user
        """
        data = request.args

        categoryToBeDeletedName = data.get('name')

        try:
            categoryToBeDeleted = Category.query.filter_by(name=categoryToBeDeletedName).first()
            if categoryToBeDeleted:
                db.session.delete(categoryToBeDeleted)
                db.session.commit()
            else:
                return {'message': 'category not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'category has been deleted successfully.'}, 201
