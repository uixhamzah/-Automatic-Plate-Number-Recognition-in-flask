import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt, mail
from flask_mail import Message
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, RegistrationLoginForm, PostForm
from flaskblog.models import User, LUser
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.product import main
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'flaskblog/static/uploads/'

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/anpr', methods=['GET', 'POST'])
@login_required
def anpr():
    form = PostForm()
    if form.validate_on_submit():
        flash("File  uploaded successfully", 'success')
        filename=secure_filename(form.picture.data.filename)
        picture_path = os.path.join(app.root_path, 'static/uploads', filename)
        i = Image.open(form.picture.data)
        i.save(picture_path)
        extracted_output=main(picture_path)
        print("####################################################")
        print(extracted_output)
        print("####################################################")
        user=User.query.filter_by(licenceplate=extracted_output).first()
        image_file = url_for('static', filename='uploads/' + filename)
        if user :
            flash("Your vehicle is authorized",'success')
            return render_template('uploadPlateNumber/anpr.html', form=form, label=extracted_output, img_src=image_file)
        else:
            flash("Your vehicle is not registered", 'danger')
            message= Message('Vehicle not registered',sender=current_user.email, recipients=['authority@gmail.com'])
            message.body = extracted_output
            # mail.send(message)
            return render_template('uploadPlateNumber/anpr.html', form=form, label=extracted_output, img_src=image_file, msg="Please register your vehicle!")

        return redirect(url_for('anpr'))
    return render_template('uploadPlateNumber/anpr.html',form=form)

@app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, licenceplate=form.licenceplate.data)
        db.session.add(user)
        db.session.commit()
        message= Message("Vehicle registered",sender=current_user.email, recipients=[form.email.data])
        message.body = form.licenceplate.data
        # mail.send(message)
        flash(f'Your vehicle registered and an Email is send to {form.email.data}! ', 'success')
        return redirect(url_for('anpr'))
    return render_template('register.html', form=form)

@app.route("/newlogin", methods=['GET', 'POST'])
def newlogin():
    if current_user.is_authenticated:
        flash('You are currently Logged in', 'success')
        return redirect(url_for('dashboard'))
    form = RegistrationLoginForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = LUser(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('New CheckPost registered!', 'success')
        return redirect(url_for('login'))
    return render_template('newlogin.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are currently Logged in', 'success')
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = LUser.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You are Logged out', 'success')
    return redirect(url_for('dashboard'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',image_file=image_file, form=form)
