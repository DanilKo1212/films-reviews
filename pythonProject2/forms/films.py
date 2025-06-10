from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.simple import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea


class EditFilmsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    description = StringField('Description', widget=TextArea(), validators=[DataRequired()])
    image = FileField('Image',
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Выберите изображение')])
    submit = SubmitField('Done')