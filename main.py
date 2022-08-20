from flask import Flask, render_template, redirect, request


app = Flask(__name__)

@app.route("/")
def home():

    return render_template("index.html")


@app.route("/projects")
def projects():
    return render_template('projects.html')


@app.route("/blog")
def blog():
    current_path = request.path
    return render_template("blog.html")


if __name__ == '__main__':
    app.run(debug=True)