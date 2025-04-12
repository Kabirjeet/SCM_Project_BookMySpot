from flask import Blueprint,render_template, request, flash, redirect, url_for, current_app, session
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
import random
import string
import requests

auth = Blueprint('auth', __name__)

# ----------------------------------------EMAIL VERIFICATION--------------------------------

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()    #   .first() Shows 1st result
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
                # return redirect(url_for('views.emailotp'))
                # return redirect(url_for('auth.emailotp',user=current_user))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        fname = request.form.get('fname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()    #   .first() Shows 1st result
        if user:
            flash('Email already exists.', category='error')
        else:
            if len(email) < 4:
                flash('Invalid Email', category='error')
            elif len(fname) < 2:
                flash('Name must be greater than 1 character', category='error')
            elif len(password1) < 7:
                flash('Password must be atleast 7 characters', category='error') 
            elif password1 != password2:
                flash('Passwords should match', category='error')
            else:
                new_user = User(email = email, fname = fname, password = generate_password_hash(password1, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()
                # login_user(user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('auth.login')) # or url_for('/')


    return render_template("sign_up.html", user=current_user)

# ----------------------------------------------------Email Route-------------------------------

@auth.route('/book_tickets', methods=['POST'])
def book_tickets():
    movie = request.form.get('movie')
    date = request.form.get('date')
    city = request.form.get('city')
    cinema = request.form.get('cinema')
    category = request.form.get('Category')
    ticketsnum = int(request.form.get('ticketsnum'))
    time = request.form.get('Time')
    
    # Determine price based on the category
    price_per_ticket = 0
    if category == "silver":
        price_per_ticket = 120
    elif category == "gold":
        price_per_ticket = 180
    elif category == "platinum":
        price_per_ticket = 240

    price = price_per_ticket * ticketsnum
    tax = 0.18*price
    total_payable = price + tax

    # Email message

    recipient_email = current_user.email

    msg = Message(
        'Your Ticket Booking Confirmation',
        sender='kabirjeet0370.becse24@chitkara.edu.in',
        recipients=[recipient_email]  
    )
    msg.body = f'''
    Movie: {movie}
    Show Date: {date}
    Show Time: {time}
    City: {city.capitalize()}
    Cinema: {cinema}
    Seat Category: {category.capitalize()}
    Number of Tickets: {ticketsnum}
    Price Per Ticket: Rs.{price_per_ticket}
    Total Amount Payable (Inc. all Taxes): Rs.{total_payable}
    '''
    
    # Send the email
    # mail.send(msg)
    
    # return 'Email sent!'

    mail = current_app.extensions.get('mail') 
    if mail:
        mail.send(msg)
        flash('Booking Confirmation Email Sent Successfully to registered email address!', category='success')
        return redirect(url_for('views.home')) # or url_for('/')
        # return 'Email sent!'
    else:
        flash('Email service is not configured properly.', category='error')
        return redirect(url_for('auth.book_tickets'))
    
# ------------------------------------------------------Reset Password------------------------------------------

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        otp = request.form.get('otp')
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if email and not otp and not new_password:
            user = User.query.filter_by(email=email).first()
            if user:
                generated_otp = generate_otp()
                session['otp'] = generated_otp
                session['otp_email'] = email

                msg = Message(
                    'Your OTP for Password Reset',
                    sender='kabirjeet0370.becse24@chitkara.edu.in',
                    recipients=[email]
                )
                msg.body = f"Your OTP is: {generated_otp}"
                mail = current_app.extensions.get('mail')
                if mail:
                    mail.send(msg)
                    flash('OTP sent to your email. Please enter the OTP to proceed.', category='success')
                    return render_template("reset_password.html", email=email, show_otp_field=True, user=current_user)
                else:
                    flash('Email service is not configured properly.', category='error')
            else:
                flash('Email does not exist.', category='error')

        elif email and otp and not new_password:
            if otp == session.get('otp') and email == session.get('otp_email'):
                flash('OTP verified! You can now reset your password.', category='success')
                return render_template("reset_password.html", email=email, show_password_fields=True, user=current_user)
            else:
                flash('Invalid OTP. Please try again.', category='error')
                return render_template("reset_password.html", email=email, show_otp_field=True, user=current_user)

        elif email and new_password and confirm_password:
            if new_password == confirm_password and len(new_password) >= 7:
                user = User.query.filter_by(email=email).first()
                if user:
                    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                    db.session.commit()
                    session.pop('otp', None)
                    session.pop('otp_email', None)
                    flash('Password reset successfully!', category='success')
                    return redirect(url_for('auth.login'))
                else:
                    flash('An error occurred. Please try again.', category='error')
            else:
                flash('Passwords do not match or are too short.', category='error')

    return render_template("reset_password.html", show_otp_field=False, show_password_fields=False, user=current_user)

# ----------------------------------------------------------Search Movie--------------------------------------------

@auth.route('/search_movies', methods=['GET'])
def search_movies():
    query = request.args.get('query')
    api_key = "44905570c15e2962f494748d812e8a95"
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"

    response = requests.get(url)
    if response.status_code == 200:
        movies = response.json().get('results', [])
    else:
        movies = []
        flash("Failed to fetch movie results. Try again later.", "error")

    for movie in movies:
        movie['poster_url'] = f"https://image.tmdb.org/t/p/w200{movie['poster_path']}" if movie.get('poster_path') else None

    return render_template('search_results.html', movies=movies, user=current_user)


# ------------------------------------------------------English Routes----------------------------------------------

@auth.route('/bookfastandfurious')
def bookfastandfurious():
    return render_template("bookfastandfurious.html", user=current_user)

@auth.route('/bookprey')
def bookprey():
    return render_template("bookprey.html", user=current_user)

# -------------------------------------------------------Hindi Routes-----------------------------------------------

@auth.route('/bookarticle370')
def bookarticle370():
    return render_template("bookarticle370.html", user=current_user)

@auth.route('/bookshaitaan')
def bookshaitaan():
    return render_template("bookshaitaan.html", user=current_user)

@auth.route('/bookchhaava')
def bookchhaava():
    return render_template("bookchhaava.html", user=current_user)

@auth.route('/booksrikanth')
def booksrikanth():
    return render_template("booksrikanth.html", user=current_user)

# -------------------------------------------------------Punjabi Routes----------------------------------------------

@auth.route('/bookjattandjuliet3')
def bookjattandjuliet3():
    return render_template("bookjattandjuliet3.html", user=current_user)

@auth.route('/bookardaas_sdbd')
def bookardaas_sdbd():
    return render_template("bookardaas_sdbd.html", user=current_user)

@auth.route('/bookShindaShindanopapa')
def bookShindaShindanopapa():
    return render_template("bookShindaShindanopapa.html", user=current_user)

@auth.route('/bookRoseRoseyteGulab')
def bookRoseRoseyteGulab():
    return render_template("bookRoseRoseyteGulab.html", user=current_user)

# ------------------------------------------------------Upcoming Movies----------------------------------------------
@auth.route('/upcomingpunjab95')
def upcomingpunjab95():
    return render_template("upcomingpunjab95.html", user=current_user)