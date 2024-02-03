from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text,ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import CreatePostForm,Register
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required
db = SQLAlchemy()
class User(UserMixin,db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(250), nullable=False)
    mail: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    pass_word: Mapped[str] = mapped_column(String(250), nullable=False)
    posts = relationship("BlogPost",back_populates="author")
    comments = relationship("Comments",back_populates="comment_author")

class Comments(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id :Mapped[int] = mapped_column(Integer,ForeignKey("user.id"))
    comment_author = relationship("User",back_populates="comments")
    blog_post = relationship("BlogPost",back_populates="comments")
    post_id : Mapped[int]  = mapped_column(Integer, db.ForeignKey("blog_posts.id"))


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id :Mapped[int] = mapped_column(Integer,ForeignKey("user.id"))
    author = relationship("User", back_populates="posts")
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments = relationship("Comments",back_populates="blog_post")
