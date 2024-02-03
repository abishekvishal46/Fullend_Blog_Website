from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField,PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField



class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
class Register(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])

    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let me in!")
class CommentForm(FlaskForm):
     comments = CKEditorField("comments")
     submit = SubmitField("Submit")

# TODO: Create a LoginForm to login existing users


# TODO: Create a CommentForm so users can leave comments below posts
