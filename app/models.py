from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User{self.username}'


class Pitch(db.Model):
    __tablename__='pitches'

    id = db.Column(db.Integer,primary_key = True) 
    name = db.Column(db.String(255))
    content = db.Column(db.String())
    owner = db.Column(db.String())
    category = db.Column(db.String())
    # date = db.Column(db.DateTime,default=datetime.utcnow)
    users = db.relationship('User',backref ='pitch',lazy='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_pitches(cls):
        '''
        Function that queries the database and returns all the pictches
        '''
        return Pitch.query.all()

    @classmethod
    def get_pitches_by_category(cls,category_id):
        '''
        Function that queries the database and returns the pitches based on the category passed to it
        '''
        
        return Pitch.query.filter_by(category_id=category_id)      
    def __repr__(self):
                return f"Pitch {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment_content = db.Column(db.String())
    # posted = db.Column(db.DateTime,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_comment(self):
            db.session.add(self)
            db.session.commit()

    @classmethod
    def get_comments(cls,id):
            comments = Comment.query.filter_by(pitch_id=id).all()
            return comments
                
    def __repr__(self):
        return f'COMMENT {self.comment_content}'