from unicodedata import category
from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import Post
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("index.html", name=current_user.username, user=current_user, posts=posts)

@views.route("/create-post", methods=["GET","POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")
        
        if not text:
            flash("Post cannot be empty", category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")
            return redirect(url_for("views.home"))
    
    return render_template("create_post.html", user=current_user)

@views.route("/delete-post/<id>", methods=["GET","POST"])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    
    if not post:
        flash("Post does not exist!", category="error")
    elif current_user.id != post.author :
        flash("You don't have permission to delete this post.")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted!", category="success")
        
    return redirect(url_for("views.home"))
        
