from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from sqlalchemy import select
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text,ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import CreatePostForm,Register,LoginForm,CommentForm
from models import db,BlogPost,User,Comments


'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor()

Bootstrap5(app)
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

login_manager = LoginManager()

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.db'

db.init_app(app)
login_manager.init_app(app)
ckeditor.init_app(app)


with app.app_context():
    db.create_all()
def admin_only(f):
    @wraps(f)
    def decorated_function(*arg,**kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*arg,**kwargs)
    return decorated_function
@login_manager.user_loader
def load_user(user_id):
    # Example implementation, replace with your actual user loading logic
    return db.get_or_404(User,user_id)



@app.route('/register',methods=["POST","GET"])
def register():
    reg_form=Register()

    if reg_form.validate_on_submit():
        user_info = db.session.execute(db.select(User).where(reg_form.email.data == User.mail))
        user = user_info.scalars()
        if user:
            flash("This E-mail Already exits", "error")
        if  reg_form.password.data == reg_form.confirm_password.data :
           new_user = User(

            user_name=reg_form.username.data,
            mail = reg_form.email.data,
            pass_word=generate_password_hash(password=reg_form.password.data,method='pbkdf2:sha256')
            )

           db.session.add(new_user)
           db.session.commit()
           login_user(new_user)


           return redirect(url_for('get_all_posts'))


        else:
            flash(message="Password does'nt match",category="error")


    return render_template("register.html",form=reg_form)



@app.route('/login',methods=["POST","GET"])
def login():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.mail  == log_form.email.data))

        user = result.scalar()




        if user :
            if check_password_hash(user.pass_word, log_form.password.data):
             flash("Welcome back, You're in", "success")
             login_user(user)
            else:
                flash("Incorrect password","error")

        else:

            flash("User doesn't exits","error")
        return redirect(url_for('get_all_posts'))
    return render_template("login.html",form = log_form,current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():

    result = db.session.execute(db.select(BlogPost))



    posts = result.scalars().all()


    return render_template("index.html", all_posts=posts)




@app.route("/post/<int:post_id>",methods=["POST","GET"])

def show_post(post_id):

    com_form = CommentForm()
    current_post = db.get_or_404(BlogPost,post_id)
    if current_user.get_id() == None:

        flash(message="You Need to login to see the post",category="error")
        return redirect(url_for('login'))
    if com_form.validate_on_submit():
        new_comment = Comments(text = com_form.comments.data,blog_post = current_post,comment_author =current_user )
        print(new_comment.author_id)
        db.session.add(new_comment)
        db.session.commit()
    # if com_form.validate_on_submit():
    result = db.session.execute(db.select(Comments).where(Comments.post_id == post_id))



    all_comments= result.scalars().all()
    requested_post = db.get_or_404(BlogPost, post_id)

    return render_template("post.html", post=requested_post,form=com_form,comments=all_comments)




@app.route("/add_new_post", methods=["GET", "POST"])
@login_required
@admin_only

def add_new_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        print(new_post.author_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)



@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)



@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
