from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_from_directory, abort
from werkzeug.utils import secure_filename
import os
from datetime import datetime

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %B %Y")

@app.route("/")
def index():
    print(f"Flask ENV is set to: {app.config['ENV']}")

    return render_template("public/index.html")

@app.route("/jinja")
def jinja():

    my_name = "luuk"

    age = 16

    langs = ["Python", "Js", "Go", "Java"]

    friends = {
        "Tom": 30,
        "Amy": 40,
        "Tony": 50,
        "Theo": 63,
        "Luuk": 55,
    }

    colours = ("red", "green")

    cool = True

    class GitRemote:
        def __init__(self, name, description, url):
            self.name = name
            self.description = description
            self.url = url

        def pull(self):
            return f"Pulling repo {self.name}"

        def clone(self):
            return f"Cloning into {self.url}"

    my_remote = GitRemote(
        name="Flask Jinja",
        description="Template Design Tutorial",
        url="https://github.com.luukdej"
    )

    def repeat(x, quantity):
        return x * quantity

    date = datetime.utcnow()

    my_html = "<h1>THIS IS SOME HTmL</h1>"

    susp = "<script>alert('You got hacked')</script>"

    return render_template(
    "public/jinja.html", my_name=my_name, age=age,
    langs=langs, friends=friends, colours=colours,
    cool=cool, GitRemote=GitRemote, repeat=repeat,
    my_remote=my_remote, date=date, my_html=my_html,
    susp=susp,
    )

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        req = request.form
        username = req["username"]
        email = req.get("email")
        password = request.form["password"]
        print(username, email, password)
        return redirect(request.url)
    return render_template("public/signup.html")


users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creatof of the Flask framework",
        "twitter_handle": "@mitsuhiko"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "elon musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk"
    }
}

@app.route("/profile/<username>")
def profile(username):

    user = None

    if username in users:
        user = users[username]

    return render_template("public/profile.html", username=username, user=user)

@app.route("/json", methods=["POST"])
def json_example():

    if request.is_json:

        req = request.get_json()

        response_body = {
            "message": "JSON received!",
            "sender": req.get("name")
        }

        res = make_response(jsonify(response_body), 200)

        return res

    else:

        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)
    return res

@app.route("/query")
def query():

    if request.args:
        args = request.args

        if "title" in args:
            title = request.args.get("title")

        print(title)
    return "Query received", 200

def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("This image extension is not supported.")
                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            print("Image saved.")

            return redirect(request.url)

    return render_template("public/upload_image.html")


@app.route("/get-image/<path:image_name>")
def get_image(image_name):

    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=False
            )

    except FileNotFoundError:
        abort(404)

@app.route("/get-csv/<path:filename>")
def get_csv(filename):

    try:
        return send_from_directory(
            app.config["CLIENT_CSV"], filename=filename, as_attachment=True
            )

    except FileNotFoundError:
        abort(404)

@app.route("/get-report/<path:path>")
def get_report(path):

    try:
        return send_from_directory(
            app.config["CLIENT_REPORTS"], filename=path, as_attachment=True
            )

    except FileNotFoundError:
        abort(404)
