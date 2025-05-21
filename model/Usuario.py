from extensoes import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    postcode = db.Column(db.String(20))
    city = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    cargo = db.Column(db.String(100))
    email = db.Column(db.String(120))
    others = db.Column(db.Text)
    website = db.Column(db.String(120))
