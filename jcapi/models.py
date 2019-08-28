from jcapi import db, bcrypt


contract_party = db.Table('contract_parties',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False), # noqa
    db.Column('contract_id', db.Integer, db.ForeignKey('contracts.id'), nullable=False) # noqa
)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    contracts = db.relationship("Contract",
                                secondary=contract_party,
                                lazy=True,
                                back_populates="parties")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class TemplateTag(db.Model):

    __tablename__ = 'template_tags'

    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            'id': self.id,
            'contract_id': self.contract_id,
            'name': self.name,
            'value': self.value
        }


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
    parties = db.relationship("User",
                              secondary=contract_party,
                              lazy=True,
                              back_populates="contracts")
    template_tags = db.relationship("TemplateTag", uselist=True, backref='contract', lazy=True)
    # relation versions

    def to_dict(self):
        return {
            'id': self.id,
            'version': self.version,
            'name': self.name,
            'legal_text': self.legal_text,
            'description': self.description,
            'effective_date': self.effective_date,
            'expiration_date': self.expiration_date,
            'currency': self.currency,
            'status': self.status,
            'owner_id': self.owner_id,
            'parties': [u.to_dict() for u in self.parties],
            'template_tags': [tt.to_dict() for tt in self.template_tags]
        }
