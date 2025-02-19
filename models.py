from app import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), nullable=False)
    avatar = db.Column(db.String(120))
    discriminator = db.Column(db.String(4))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
