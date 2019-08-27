from jcapi import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')


class Contract(db.Model):

    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer)
    name = db.Column(db.String(128))
    description = db.Column(db.Text())
    legal_text = db.Column(db.Text())
    effective_date = db.Column(db.Date())
    expiration_date = db.Column(db.Date())
    currency = db.Column(db.String(3))
    status = db.Column(db.String(32))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # template tags
    # relation versions
