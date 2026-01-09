#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User, UserSchema

user_schema = UserSchema()

class Signup(Resource):
    def post(self):
        data = request.get_json()

        user = User(username=data["username"])
        user.password_hash = data["password"]

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        
        return make_response(user_schema.dump(user), 201)
    

class Login(Resource):
    def post(self):
        data = request.get_json()

        user = User.query.filter(User.username == data["username"]).first()

        if user and user.authenticate(data["password"]):
            session["user_id"] = user.id
            return make_response(user_schema.dump(user), 200)

        return make_response({"error": "Invalid username or password"}, 401)
    

class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        return make_response("", 204)
    

class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")

        if user_id:
            user = User.query.get(user_id)
            if user:
                return make_response(user_schema.dump(user), 200)
            
        return make_response("", 204)


class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None
        return make_response("", 204)

api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(ClearSession, "/clear", endpoint="clear")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
