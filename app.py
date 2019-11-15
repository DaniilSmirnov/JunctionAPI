from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import request
import mysql.connector
from flask_cors import CORS
import json

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin: *'

cors = CORS(app)
api = Api(app)

cnx = mysql.connector.connect(user='root', password='i130813',
                                  host='127.0.0.1',
                                  database='junction')


class TestConnection(Resource):
    def get(self):
        return {'status': 'success'}


class GetWishlists(Resource):
    def get(self):
        cursor = cnx.cursor()

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        args = parser.parse_args()

        user_id = args['user_id']

        query = "select * from wishlists where iduser = %s;"
        data = (user_id, )
        cursor.execute(query, data)
        wishlist = {}
        responce = []
        for item in cursor:
            i = 0
            for value in item:
                if i == 0:
                    wishlist.update({'id': value})
                    id = value
                if i == 1:
                    wishlist.update({'user_id': value})
                if i == 2:
                    wishlist.update({'name': value})

                products = []

                query = "select id product from products where idwishlist = %s;"
                data = (id, )
                cursor.execute(query, data)
                for item in cursor:
                    for value in item:
                        products.append(value)

                wishlist.update({'products': products})

                i += 1

                responce.append(wishlist)
        cursor.close()
        return responce


class AddWishlist(Resource):
    def post(self):
        cursor = cnx.cursor()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=int)
            parser.add_argument('name', type=str)
            args = parser.parse_args()

            user_id = args['user_id']
            name = args['name']

            query = "insert into wishlists values (default, ?, ?);"
            data = (user_id, name)
            cursor.execute(query, data)
            cnx.commit()
            cursor.close()
            return {'status': 'success'}
        except BaseException as e:
            cursor.close()
            return {'status': str(e)}


api.add_resource(TestConnection, '/TestConnection')
api.add_resource(GetWishlists, '/GetWishlists')
api.add_resource(AddWishlist, '/AddWishlist')


if __name__ == '__main__':
    app.run(debug=True)