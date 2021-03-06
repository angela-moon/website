from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import url_for
from flask_login import current_user
from flask_login.utils import login_required
from .models import Post
from datetime import datetime
from . import db

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html", user=current_user, type="static")

@views.route("/about")
def about():
    return render_template("about.html", user=current_user, type="static")

@views.route("/blog")
def blog():
    posts = Post.query.all()
    return render_template("blog.html", user=current_user, posts=posts, type="static")

@views.route("/projects")
def projects():
    return render_template("project.html", user=current_user, type="static")

@views.route("/projects/mini-programs")
def mini_programs():
    return render_template("projects/mini-programs.html", user=current_user, type="static")

@views.route("/projects/cs-projects")
def cs_projects():
    return render_template("projects/cs-projects.html", user=current_user, type="static")

@views.route("/projects/fashion-design")
def fashion_design():
    return render_template("projects/fashion-design.html", user=current_user, type="static")

@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        subtitle = request.form.get("subtitle")
        date_created = request.form.get("date_created")
        date_created = datetime.strptime(date_created, "%Y-%m-%d")
        if not title:
            flash("Title cannot be empty.")
        elif not subtitle:
            flash("Subtitle cannot be empty.")
        elif not text:
            flash("Post cannot be empty.")
        else:
            if not date_created:
                post = Post(title=title, subtitle=subtitle, text=text, date_created=datetime.now())
                db.session.add(post)
                db.session.commit()
            else:
                post = Post(title=title, subtitle=subtitle, text=text, date_created=date_created)
                db.session.add(post)
                db.session.commit()
            flash("Post created!")
            return redirect(url_for("views.blog"))
    return render_template("create_post.html", user=current_user, type="static")

@views.route("/edit-post/<id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        subtitle = request.form.get("subtitle")
        date_created = request.form.get("date_created")
        if not title:
            flash("Title cannot be empty.")
        elif not subtitle:
            flash("Subtitle cannot be empty.")
        elif not text:
            flash("Post cannot be empty.")
        else:
            if date_created:
                date_created = datetime.strptime(date_created, "%Y-%m-%d")
                post.date_created = date_created
            post.title = title
            post.text = text
            post.subtitle = subtitle
            post.date_edited = datetime.now()
            db.session.commit()
            flash("Post edited!")
            return redirect(url_for("views.blog"))
    return render_template("edit_post.html", user=current_user, type="static", post=post)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    
    if not post:
        flash("Post does not exist.")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.")
        
    return redirect(url_for("views.home"))

@views.route("/post/<id>")
def view_post(id):
    post = Post.query.filter_by(id=id).first()
    return render_template("post.html", user=current_user,post=post, type="static")