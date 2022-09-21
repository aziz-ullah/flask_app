import json
from msilib import schema
import re
from unittest import result
from flask import Flask,jsonify,request,render_template
from flask_sqlalchemy import SQLAlchemy
from webargs import fields,validate
from webargs.flaskparser import use_args
from marshmallow import Schema


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50),nullable = False)
    email = db.Column(db.String(80),unique = True,nullable = False)
    
    def __repr__(self):
        return '<User>' + self.username
    
class UserSchema(Schema):
    username = fields.String(required=True,validate=validate.Length(min=5))
    email = fields.Email(required = True)
    
    
@app.route('/user',methods = ["POST"])
@use_args(UserSchema,location="json")
def add_user(kwargs):
    try:
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return 'User added'
    except Exception as e:
        return 'User Not Added'
    
@app.route('/user',methods = ["GET"])
def get_all_users():
    users = db.session.query(User).all()
    return render_template('table.html',users = users)

@app.route('/user',methods = ["PUT"])
def update_user():
    try:
        user = db.session.query(User).filter(User.id == request.json["id"]).first()
        if "username" in request.json:
            user.username = request.json["username"]
        
        if "email" in request.json:
            user.email = request.json["email"]
            
        db.session.commit()
        return "User Updated"
    except Exception as e:
        print(e)
        return "User not Updated"
    
@app.route('/user',methods = ["DELETE"])
def delete_user():
    try:
        user = db.session.query(User).filter(User.id == request.json["id"]).first()
        db.session.delete(user)
        db.session.commit()
        
        return "User Deleted",200
    except Exception as e:
        print(e)
        return "User not Deleted",422

        

    


if __name__ == '__main__':
    app.run(debug=True)