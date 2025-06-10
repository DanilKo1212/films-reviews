from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.simple import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea


class EditReviewForm(FlaskForm):
    body = StringField('Review', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Done')
