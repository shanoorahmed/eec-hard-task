from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'idonotknow!!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True)
    date_posted = db.Column(db.DateTime)
    post = db.Column(db.Text)

class Addpost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=20)])
    post = TextAreaField('Post', validators=[DataRequired()])

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('index.html', posts=posts)

@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    form = Addpost()
    if form.validate_on_submit():
        new_post = Blogpost(title=form.title.data, date_posted=datetime.now(), post=form.post.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('addpost.html', form=form)

@app.route('/viewpost/<int:post_id>')
def viewpost(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('viewpost.html', post=post)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'),500