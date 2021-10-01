from taskmanager import db


class User(db.Model):
    # schema for the User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    # Hashed password is a lot longer than the typed in password!
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship(
        "Task",
        backref="user",
        cascade="all, delete",
        lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.username


class Category(db.Model):
    # schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False)
    tasks = db.relationship(
        "Task",
        backref="category",
        cascade="all, delete",
        lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.category_name


class Task(db.Model):
    # schema for the Task model
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True, nullable=False)
    task_description = db.Column(db.Text, nullable=True)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "category.id", ondelete="CASCADE"
        ), 
        nullable=False)
    task_owner_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id", ondelete="CASCADE"
        )
    )

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return f'#{self.id} Task: {self.task_name} | Urgent: {self.is_urgent}'
