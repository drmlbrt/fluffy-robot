from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def safe_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.remove(self)
        db.session.commit()

    @classmethod  # We are using the class User inside the method, so change to classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()  # SELECT * FROM items WHERE name=name LIMIT 1