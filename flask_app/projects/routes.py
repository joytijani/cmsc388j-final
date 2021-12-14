from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
from .. import project_client
from ..forms import PostForm, ContactForm
from ..models import User, Post, Project
from ..utils import current_time
projects = Blueprint('projects', __name__)
import  base64

@projects.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@projects.route("/projects", methods=["GET", "POST"])
def project():
    try:
        username = current_user.username
        projects = project_client.fetch_projects(username)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("{{page_not_found(e)}}"))
    if Project.objects() == None:
        for project in projects:
            proj = Project(
                project_id = project.id,
                title = project.title,
                github_url = project.url,
                description = project.description,
            )
            proj.save()
    
    return render_template("projects.html", projects=projects, forloop = 1)

@projects.route("/aboutme", methods=["GET", "POST"])
def about_me():
    return render_template("about_me.html")


@projects.route("/projects/<project_id>", methods=["GET", "POST"])
def project_detail(project_id):
    try:
        result = Project.objects(project_id = project_id).first()
        print(result)
    except ValueError as e:
        return render_template("project_detail.html", error_msg=str(e))

    form = PostForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        post = Post(
            commenter = current_user._get_current_object(),
            project_title = result.title,
            date=current_time(),
            text = form.text.data,
        )
        post.save()
    
        return redirect(request.path)
    posts = list(Post.objects(project_title = result.title))
    return render_template(
        "project_detail.html", form = form, project = result, posts = posts
    )

@projects.route('/contact', methods=["GET","POST"])
def contact():
    form = ContactForm()
    # here, if the request type is a POST we get the data on contat
    #forms and save them else we return the contact forms html page
    if request.method == 'POST':
        return 'Form posted.'
    else:
        return render_template('contact.html', form=form)

@projects.route("/user/<username>")
def user_detail(username):
    user = User.objects(username = username).first()
    posts = Post.objects(commenter = user)

    return render_template("user_detail.html", username = username, posts = posts)
