from flask_wtf import FlaskForm 
from wtforms import SubmitField,TextAreaField,StringField,SelectField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Add or Update your bio so that we get to know you.',validators = [Required()])
    submit = SubmitField('Submit')

class AddPitch(FlaskForm):
    title = StringField("Pitch Title", validators = [Required()])
    category = SelectField("What category are you submitting to?", choices=[("Twitter", "Twitter Pitches"), ( "Elevator", "Elevator Pitches"), ("Competition", "Competition Pitches"), ("Business", "Business Pitches"),("Technology", "Technology Pitches")],validators=[Required()])
    content = TextAreaField('What pitch do you want to share?',validators = [Required()] )
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment_content = TextAreaField('Add a comment',validators = [Required()] )
    submit = SubmitField('Submit')
