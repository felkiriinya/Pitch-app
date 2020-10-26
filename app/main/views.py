from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch,Comment,Upvote,Downvote
from .forms import UpdateProfile,AddPitch,CommentForm,UpvoteForm,Downvote
from .. import db,photos
from flask.views import View,MethodView

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


# @main.route('/user/<pitchname>/pitch',methods = ['GET','POST'])

# def addapitch(pitchname):
    
#     form = AddPitch()

#     if form.validate_on_submit():
        
#         pitch = Pitch(content=form.content.data,name=form.title.data, category = form.category.data)
#         # db.session.add(pitch)
#         # db.session.commit()
#         pitch.save_pitch()


#         flash('Your pitch has been posted!', 'success')
#         return redirect(url_for('main.categories',pitchname=pitch.name))

#     title = 'Add a new Pitch'
#     return render_template('add_pitch.html',form =form, title = title)        

@main.route('/categories')
def categories():


    title = 'Pitches | Categories'
    pitch = Pitch.query.filter_by().first()
    twitter = Pitch.query.filter_by(category="twitter")
    elevator = Pitch.query.filter_by(category = "elevator")
    competition = Pitch.query.filter_by(category = "competition")
    investor = Pitch.query.filter_by(category = "investor")
    upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
    # downvotes = Downvote.get_all_downvotes(pitch_id=Pitch.id)
    

    return render_template('categories.html',title =title, pitch = pitch, twitter=twitter, elevator= elevator, competition = competition, investor = investor, upvotes=upvotes )

# @main.route("/comment", methods=['GET', 'POST'])
# def new_comment():
#     title = 'New Comment | Pitch'
#     form = CommentForm()
#     # categories = Category.query.all()
#     # pitch = Pitch.query.filter_by(id).first()
#     if form.validate_on_submit():
#         comment = Comment(comment_content=form.comment_content.data)
#         db.session.add(comment)
#         db.session.commit()
#         flash('Your comment has been added!', 'success')
#         return redirect(url_for('main.categories'))

#     return render_template('add_comment.html', title=title, comment_form=form)

@main.route('/pitches/new/', methods = ['GET','POST'])
# @login_required
def new_pitch():
    form = AddPitch()
    my_upvotes = Upvote.query.filter_by(pitch_id = Pitch.id)
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        # owner_id = current_user
        category = form.category.data
        # print(current_user._get_current_object().id)
        new_pitch = Pitch(title = title,description=description,category=category)
        db.session.add(new_pitch)
        db.session.commit()
        
        
        return redirect(url_for('main.categories'))
    return render_template('add_pitch.html',form=form)




@main.route('/comment/new/<int:pitch_id>', methods = ['GET','POST'])

def new_comment(pitch_id):
    form = CommentForm()
    pitch=Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, pitch_id = pitch_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', pitch_id= pitch_id))

    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    return render_template('add_comment.html', form = form, comment = all_comments, pitch = pitch )


@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods = ['GET', 'POST'])

def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.categories'))


    new_upvote = Upvote(pitch_id=pitch_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.categories'))



@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods = ['GET', 'POST'])
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Downvote.query.filter_by(pitch_id = pitch_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.categories'))


    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.categories'))

