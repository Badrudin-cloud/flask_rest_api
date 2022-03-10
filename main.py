from dataclasses import fields
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/test1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(30))
    reg = db.Column(db.DateTime)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.reg = datetime.now()
    
    def __repr__(self):
        return f"<User {self.username}>"


# new_user = User('Badar', 'Badar@gmail.com', '1234')
# db.session.add(new_user)
# User.query.filter_by(id=6).delete()
# user = User.query.get('1')
# user.username = 'Zakariye'
# db.session.commit()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'reg')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/add', methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Saved'})


@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    result = user_schema.dump(user)
    return jsonify(result)

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    reg = request.json['reg']
    user = User.query.get(id)
    user.username = username
    user.email = email
    user.password = password
    user.reg = reg
    db.session.commit()
    
    return jsonify({'msg': 'updated'})


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    
    return jsonify({'msg': 'deleted'})


if __name__ == '__main__':
    app.run(debug=True)