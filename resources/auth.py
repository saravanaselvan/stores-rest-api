from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from resources.user import UserModel
from werkzeug.security import safe_str_cmp

from security import authenticate


class Login(Resource):

    def post(self):
        request_data = request.get_json()
        user = authenticate(request_data['username'], request_data['password'])

        if user:
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token)

        return {"message": "Invalid credentials"}, 401


class SignUp(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        print(parser)
        # parser.add_argument('username', type=string,
        # required=True, help="This field is required")
        # parser.add_argument('password', type=string,
        #                     required=True, help="This field is required")
        # parser.add_argument('confirm_password', type=string,
        #                     required=True, help="This field is required")
        data = request.get_json()
        print(data)

        if safe_str_cmp(data['password'], data['confirm_password']):
            user = UserModel.create_user(data['username'], data['password'])
            return {'user': user}

        return {"message": "Signup error"}, 400
