from cerberus import Validator

from app import db

schema = {
    'fullname': {
        'type': 'string'
    },
    'index': {
        'type': 'integer'
    },
    'mail_id': {
        'type': 'string'
    },
    'weight': {
        'type': 'float'
    },
    'cost': {
        'type': 'integer'
    }
}

class Order(db.Model):
    fullname = db.Column(db.String(100))
    index = db.Column(db.Integer)
    mail_id = db.Column(db.String(50), primary_key=True, index=True)
    weight = db.Column(db.Float)
    cost = db.Column(db.Integer)

    validator = Validator(schema)

    def __repr__(self):
        return '<Order {0} - {1} - {2} - {3}>'.format(self.mail_id, self.fullname, self.weight, self.cost)

    def as_dict(self):
        return dict(fullname=self.fullname,
                    index=self.index,
                    mail_id=self.mail_id,
                    weight=self.weight,
                    cost=self.cost)

    @staticmethod
    def validate(d):
        v = Order.validator
        result = v.validate(d)
        if result:
            return {}
        return v.errors
