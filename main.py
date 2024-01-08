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


@app.route("/")
def home():
    return render_template("index.html", blog_route=False)


@app.route("/projects")
def projects():
    return render_template('projects.html', blog_route=False)


@app.route("/blog")
def blog():
    return render_template("blog.html", blog_route=False)


if __name__ == '__main__':
    app.run(debug=True)