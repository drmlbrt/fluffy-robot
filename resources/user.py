import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()  # initialize new object, run the request through the parser and match with arguments defined
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username field cannot be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password field cannot be blank"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']) is not None:
            return {"message": "User with username: '{}' already exists".format(data['username'])}, 400

        user = UserModel(**data)
        user.safe_to_db()

        return {"message": "User {} has been created".format(data['username'])}, 201
