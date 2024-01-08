from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = 'some random key'

# allows app to use bootstrap
bootstrap = Bootstrap(app)


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