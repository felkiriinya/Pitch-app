from flask_wtf import FlaskForm 
from wtforms import SubmitField,TextAreaField,StringField,SelectField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Add or Update your bio so that we get to know you.',validators = [Required()])
    submit = SubmitField('Submit')

class AddPitch(FlaskForm):
    pitcher = StringField("Submitted By: Your Name ...", validators = [Required()])
    title = StringField("Pitch Title", validators = [Required()])
    category = SelectField("What category are you submitting to?", choices=[("twitter", "Twitter"), ( "elevator", "Elevator"), ("competition", "Competition"), ("investor", "Investor")],validators=[Required()])
    description = TextAreaField('What pitch do you want to share?',validators = [Required()] )
    submit = SubmitField('Submit')
    

class CommentForm(FlaskForm):

    description = TextAreaField('Add a comment',validators = [Required()] )
    submit = SubmitField('Submit')

class UpvoteForm(FlaskForm):
	submit = SubmitField()


class Downvote(FlaskForm):
	submit = SubmitField()