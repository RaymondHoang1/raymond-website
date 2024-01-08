from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request, url_for, flash
import os
from forms import CreatePostForm, RegisterForm, LoginForm
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some random key'

db = SQLAlchemy(app)
# allows app to use bootstrap
bootstrap = Bootstrap(app)
# allows app to use ckeditor in html
ckeditor = CKEditor(app)


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)


db.create_all()


@app.route("/")
def home():
    return render_template("index.html", blog_route=False)


@app.route("/projects")
def projects():
    return render_template('projects.html', blog_route=False)


@app.route("/blog")
def blog():
    all_posts = db.session.query(BlogPost).all()
    return render_template("blog.html", blog_posts=all_posts, blog_route=True)


@app.route("/blog/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        account = User.query.filter_by(email=form.email.data).first()
        if not account:
            flash("That email does not exist, please register for an account")
            return redirect(url_for('register'))
        elif form.password.data == account.password:
            return redirect(url_for('blog'))
        else:
            flash("Wrong password please try again")
            return redirect(url_for('login'))
    return render_template("login.html", form=form, blog_route=True)


@app.route("/blog/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("This email already exists please proceed to the login page.")
            return redirect(url_for('login'))
        else:
            new_user = User(
            name = form.name.data,
            email = form.email.data,
            password = form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('blog'))
    return render_template("register.html", form=form, blog_route=True)


@app.route("/blog/new-post", methods=['GET', 'POST'])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
        author = "Raymond",
        title = form.title.data,
        subtitle = form.subtitle.data,
        body = form.body.data,
        img_url = form.img_url.data,
        date = datetime.now().strftime('%B %d, %Y'))
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template("new_post.html", form=form, blog_route=True)


@app.route("/blog/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post_to_update = BlogPost.query.filter_by(id=post_id).first()
    edit_post = CreatePostForm(title=post_to_update.title,
                    subtitle=post_to_update.subtitle,
                    img_url=post_to_update.img_url,
                    body=post_to_update.body)
    if edit_post.validate_on_submit():
        post_to_update.title = edit_post.title.data
        post_to_update.subtitle = edit_post.subtitle.data
        post_to_update.img_url = edit_post.img_url.data
        post_to_update.body = edit_post.body.data
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template("new_post.html", form=edit_post, blog_route=True)


@app.route("/blog/<int:post_id>", methods=["GET", "POST"])
def blog_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()
    return render_template("blog-post.html", post=post, blog_route=True)


if __name__ == '__main__':
    app.run(debug=True)