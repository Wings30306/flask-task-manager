from flask import render_template, request, redirect, url_for, session
from taskmanager import app, db
from taskmanager.models import Category, Task, User
# Import to secure password when storing in database
from werkzeug.security import generate_password_hash, check_password_hash
# Required import to create login_required decorator
from functools import wraps


def login_required(f):
    """
    Create @login_required decorator to make sure that
    only logged-in users can access a route
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def logout_required(f):
    """
    Create @logout_required decorator to make sure that
    only logged-out users can access a route such as login/register
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is not None:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


# Authentication routes
@app.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    """
    Function to add new user and log them in
    """
    if request.method == "POST":
        print("REQUESTED USERNAME: ", request.form["username"])
        username = request.form.get("username")
        existing_user = User.query.filter_by(username=username).first()
        print("EXISTING USER: ", existing_user)
        if existing_user:
            print("Uh oh, user with that username exists!"
                  " Did you want to log in?")
            return redirect(url_for("login"))
        elif request.form.get("password") != request.form.get("password-repeat"):
            print("Oops, passwords don't match, try again!")
            return redirect('register')
        else:
            # if username doesn't already exist in database and passwords match
            hash_pass = generate_password_hash(request.form['password'])
            user = User(username=username, password=hash_pass)
            db.session.add(user)
            db.session.commit()
            user_created = User.query.filter_by(username=username).first()
            print("Created user: ", user_created)
            session["user"] = username
            return redirect("home")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    """
    Function to log in existing users
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            print("No user with that username, please register")
            return redirect("register")
        elif not check_password_hash(existing_user.password, password):
            print("Wrong password, try again!")
            return redirect("login")
        else:  # username exist and password is correct
            session["user"] = username
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/profile", methods=["GET", "POST"])
@login_required
def home():
    """
    Show user's profile page when logged in
    """
    user = User.query.filter_by(username=session["user"]).first()
    tasks = Task.query.filter_by(task_owner_id=user.id)
    return render_template("profile.html", user=user, tasks=tasks)


@app.route("/logout")
@login_required
def logout():
    """
    Log user out when logged in
    """
    session.clear()
    return redirect(url_for("home"))


# Task routes
@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        user = User.query.filter_by(username=session["user"]).first()
        print(user)
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=bool(True if request.form.get("is_urgent") else False),
            due_date=request.form.get("due_date"),
            category_id=request.form.get("category_id"),
            task_owner_id=user.id,
            )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("add_task.html", categories=categories)


@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    user = User.query.filter_by(username=session["user"]).first()
    if task.task_owner_id == user.id:
        categories = list(Category.query.order_by(Category.category_name).all())
        if request.method == "POST":
            task.task_name=request.form.get("task_name")
            task.task_description=request.form.get("task_description")
            task.is_urgent=bool(True if request.form.get("is_urgent") else False)
            task.due_date=request.form.get("due_date")
            task.category_id=request.form.get("category_id")
            db.session.commit()
            return redirect(url_for('home'))
        return render_template("edit_task.html", task=task, categories=categories)
    return redirect(url_for("home"))


@app.route("/delete_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    user = User.query.filter_by(username=session["user"]).first()
    if task.task_owner_id == user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("home"))


# Category routes
@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template("add_category.html")


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>", methods=["GET", "POST"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))
