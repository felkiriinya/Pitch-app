from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required
from ..models import User,Pitch,Comment
from .forms import UpdateProfile,AddPitch,CommentForm
from .. import db,photos


@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    
    title = 'Pitch Deck'
    
    return render_template('index.html', title = title)

@main.route('/loggedin')
def loggedin():

    title = 'Pitch Deck'

    return render_template('loggedin.html',title =title)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    title = f'{uname} Profile'
    return render_template("profile/profile.html", user = user, title = title)

@main.route('/user/<uname>/update',methods = ['GET','POST'])

def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    title = 'Update | Profile'
    return render_template('profile/update.html',form =form, title = title)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/user/<pitchname>/pitch',methods = ['GET','POST'])
@login_required
def addapitch(pitchname):
    
    form = AddPitch()

    if form.validate_on_submit():
        
        pitch = Pitch(content=form.content.data,name=form.title.data, category = form.category.data)
        # db.session.add(pitch)
        # db.session.commit()
        pitch.save_pitch()


        flash('Your pitch has been posted!', 'success')
        return redirect(url_for('main.categories',pitchname=pitch.name))

    title = 'Add a new Pitch'
    return render_template('add_pitch.html',form =form, title = title)        

@main.route('/categories')
def categories():

    title = 'Pitches | Categories'

    return render_template('categories.html',title =title)

@main.route("/comment", methods=['GET', 'POST'])
@login_required
def new_comment():
    title = 'New Comment | Pitch'
    form = CommentForm()
    # categories = Category.query.all()
    # pitch = Pitch.query.filter_by(id).first()
    if form.validate_on_submit():
        comment = Comment(comment_content=form.comment_content.data)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.categories'))

    return render_template('add_comment.html', title=title, comment_form=form)

