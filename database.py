from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Database Models
class Employees(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    credential_id = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return '<Employee %r>' % self.id

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    credential_id = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return '<User %r>' % self.id

class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return '<Credential %r>' % self.id

class Drinks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    bev1 = db.Column(db.String(20), nullable = False)
    vol1 = db.Column(db.Integer, nullable = True)
    bev2 = db.Column(db.String(20), nullable = True)
    vol2 = db.Column(db.Integer, nullable = True)
    bev3 = db.Column(db.String(20), nullable = True)
    vol3 = db.Column(db.Integer, nullable = True)
    bev4 = db.Column(db.String(20), nullable = True)
    vol4 = db.Column(db.Integer, nullable = True)
    bev5 = db.Column(db.String(20), nullable = True)
    vol5 = db.Column(db.Integer, nullable = True)
    bev6 = db.Column(db.String(20), nullable = True)
    vol6 = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return '<Drink %r>' % self.id

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    available = db.Column(db.Integer, nullable = False)
    pump = db.Column(db.Integer, nullable = True)
    alcohol = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return '<Drink %r>' % self.id

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    drink_id = db.Column(db.Integer, nullable = False)
    pump_sequence = db.Column(db.String(20), nullable = False)
    

    def __repr__(self):
        return '<Orders %r>' % self.id

class Slots(db.Model): 
    slot = db.Column(db.Integer, primary_key = True)
    ingredient_id = db.Column(db.Integer, nullable = False)
    is_current_spout = db.Column(db.Boolean, nullable = False)
    volume = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return '<Slots %r>' % self.slot