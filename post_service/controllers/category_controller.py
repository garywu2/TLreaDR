from flask_restplus import Resource, fields, reqparse, marshal
from datetime import datetime
import uuid

from server.api.restplus import api
from server.models import db
from post_service.models.category import Category
from server.models import event_ref

ns = api.namespace('categories', description='Operations related to categories')

category_dto = api.model('category', {
    'category_uuid': fields.String(required=True, description='category uuid'),
    'name': fields.String(required=True, description='category name'),
})

category_parser = reqparse.RequestParser()
category_parser.add_argument('name', required=True, type=str, help='name of category', location='json')

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

            event_id = uuid.uuid4()
            data_set = {
                u'type': u"Category",
                u'operation': u"Add",
                u'name': new_category.name,
                u'item_id': str(new_category.category_uuid),
                u'time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")[:-3]
            }
            event_ref.document(str(event_id)).set(data_set)

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
                db.session.delete(category_to_be_deleted)
                db.session.commit()

                event_id = uuid.uuid4()
                data_set = {
                    u'type': u"Category",
                    u'operation': u"Delete",
                    u'name': category_to_be_deleted.name,
                    u'item_id': str(category_to_be_deleted.category_uuid),
                    u'time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")[:-3]
                }
                event_ref.document(str(event_id)).set(data_set)
            else:
                return {'message': 'category not found.'}, 404
        except Exception as e:
            return {"message": str(e)}, 500

        return {'message': 'category has been deleted successfully.'}, 201
