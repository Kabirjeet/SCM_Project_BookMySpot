from flask import Blueprint,render_template, request, flash, redirect, url_for, current_app
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message

# import random
# import string
# from flask import session
# from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)

# ----------------------------------------EMAIL VERIFICATION--------------------------------

# def generate_otp():
#     otp = ''.join(random.choices(string.digits, k=6))
#     return otp

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
# @auth.route('/book_tickets', methods=['POST'])
# def book_tickets():
#     city = request.form.get('city')
#     cinema = request.form.get('cinema')
#     category = request.form.get('Category')
#     ticketsnum = request.form.get('ticketsnum')
#     price_per_ticket = int(request.form.get('price_per_ticket'))
    
#     total_payable = price_per_ticket * int(ticketsnum)

#     msg = Message(
#         'Your Ticket Booking Confirmation',
#         sender='fkabirj00@gmail.com',
#         recipients=['kabir160804@gmail.com']  # Replace with the user's email
#     )
#     msg.body = f'''
#     City: {city}
#     Cinema: {cinema}
#     Seat Category: {category}
#     Number of Tickets: {ticketsnum}
#     Total Amount Payable: Rs.{total_payable}
#     '''
    
#     mail.send(msg)
    
#     return 'Email sent!'

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
        recipients=[recipient_email]  # Replace with the user's email
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

    mail = current_app.extensions.get('mail')  # Access the mail instance from current_app
    if mail:
        mail.send(msg)
        flash('Booking Confirmation Email Sent Successfully to registered email address!', category='success')
        return redirect(url_for('views.home')) # or url_for('/')
        # return 'Email sent!'
    else:
        flash('Email service is not configured properly.', category='error')
        return redirect(url_for('auth.book_tickets'))
    
# ------------------------------------------------------Reset Password------------------------------------------

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if email and not new_password:
            
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email found. You can now reset your password.', category='success')
                return render_template("reset_password.html", email=email, show_password_fields=True, user=current_user)
            else:
                flash('Email does not exist.', category='error')
                return render_template("reset_password.html", show_password_fields=False, user=current_user)

        elif email and new_password and confirm_password:
            
            if new_password == confirm_password and len(new_password) >= 7:
                user = User.query.filter_by(email=email).first()
                if user:
                    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                    db.session.commit()
                    flash('Password reset successfully!', category='success')
                    return redirect(url_for('auth.login'))
                else:
                    flash('An error occurred. Please try again.', category='error')
            else:
                flash('Passwords do not match or are too short.', category='error')
                
    return render_template("reset_password.html", show_password_fields=False, user=current_user)

# ------------------------------------------------------English Routes----------------------------------------------

@auth.route('/bookdeadpool')
def bookdeadpool():
    return render_template("bookdeadpool.html", user=current_user)

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

@auth.route('/bookstree2')
def bookstree2():
    return render_template("bookstree2.html", user=current_user)

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

