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


def search(query):
    import csv
    with open('search_index.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            item = ('  '.join(row))
            item = item.split(',')
            id = item[0]
            item = item[1]
            response = []
            if item.find(query) != -1:
                response.append(int(id))

    return response


class GetCelebrations(Resource):
    def get(self):
        cursor = cnx.cursor()

        query = "select name from celebrations where curdate() >= start and curdate() <= finish;"
        cursor.execute(query)
        response = []
        for item in cursor:
            for value in item:
                response.append(value)

        return response


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


class AddProduct(Resource):
    def post(self):
        cursor = cnx.cursor()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('wishlist_id', type=int)
            parser.add_argument('product_id', type=int)
            args = parser.parse_args()

            product_id = args['wishlist_id']
            wishlist_id = args['product_id']

            query = "insert into product values (?, ?, default);"
            data = (product_id, wishlist_id)
            cursor.execute(query, data)
            cnx.commit()
            cursor.close()
            return {'status': 'success'}
        except BaseException as e:
            cursor.close()
            return {'status': str(e)}


class AssignCategory(Resource):
    def post(self):
        cursor = cnx.cursor()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=int)
            parser.add_argument('category_id', type=int)
            args = parser.parse_args()

            user_id = args['user_id']
            category_id = args['category_id']

            query = "insert into categories values (?, ?, default );"
            data = (user_id, category_id)

            cursor.execute(query, data)
            cnx.commit()

            cursor.close()
            return {'status': 'success'}
        except BaseException as e:
            cursor.close()
            return {'status': str(e)}


class MoveProduct(Resource):
    def post(self):
        cursor = cnx.cursor()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('from_id', type=int)
            parser.add_argument('to_id', type=int)
            parser.add_argument('product_id', type=int)
            args = parser.parse_args()

            from_id = args['from_id']
            to_id = args['to_id']
            product_id = args['product_id']

            query = "update products set idwishlist = ? where idwishlist = ? and idproduct = ?;"
            data = (to_id, from_id, product_id)
            cursor.execute(query, data)
            cnx.commit()

            cursor.close()
            return {'status': 'success'}
        except BaseException as e:
            cursor.close()
            return {'status': str(e)}


class WillBePayed(Resource):
    def post(self):
        cursor = cnx.cursor()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('wishlist_id', type=int)
            parser.add_argument('choose', type=str)
            parser.add_argument('product_id', type=int)
            args = parser.parse_args()

            wishlist_id = args['wishlist_id']
            choose = args['choose']
            product_id = args['product_id']

            query = "update products set willbe = ? where idwishlist = ? and idproduct = ?;"
            data = (choose, wishlist_id, product_id)
            cursor.execute(query, data)
            cnx.commit()

            cursor.close()
            return {'status': 'success'}
        except BaseException as e:
            cursor.close()
            return {'status': str(e)}


class CheckActuality(Resource):
    def post(self):
        cursor = cnx.cursor()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=int)
            parser.add_argument('category_id', type=int)
            args = parser.parse_args()

            user_id = args['user_id']
            category_id = args['category_id']

            query = "update categories set dislikes = dislikes + 1 where iduser = ? and idcategory = ?;"
            data = (user_id, category_id)
            cursor.execute(query, data)
            cnx.commit()

            query = "select dislikes from categories where iduser = ? and idcategory = ?;"
            data = (user_id, category_id)
            cursor.execute(query, data)
            for item in cursor:
                for value in item:
                    if int(value) >= 10:
                        cursor2 = cnx.cursor()
                        query = "delete idcategories from categories where idcategories = ? and iduser = ?;"
                        data = (category_id, user_id)
                        cursor2.execute(query, data)
                        cnx.commit()

                        cursor.close()
                        cursor2.close()
                        return {'status': 'сategory removed'}

            cursor.close()
            return {'status': 'success'}
        except BaseException as e:
            cursor.close()
            return {'status': str(e)}


class FindPrefered(Resource):
    def get(self):
        cursor = cnx.cursor()

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('names', type=list)
            args = parser.parse_args()

            names = args['names']

            responce = []

            for name in names:
                responce.append(search(name))

            return responce

        except BaseException as e:
            return str(e)



api.add_resource(GetCelebrations, '/GetCelebrations')
api.add_resource(GetWishlists, '/GetWishlists')
api.add_resource(AddWishlist, '/AddWishlist')
api.add_resource(AddProduct, '/AddProduct')
api.add_resource(AssignCategory, '/AssignCategory')
api.add_resource(MoveProduct, '/MoveProduct')
api.add_resource(WillBePayed, '/WillBePayed')
api.add_resource(CheckActuality, '/CheckActuality')


if __name__ == '__main__':
    app.run(debug=True)