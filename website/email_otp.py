# from . import db
from .models import User
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user

import smtplib
import getpass

smtp_object = smtplib.SMTP('smtp.gmail.com',587)
print(smtp_object.ehlo())
print(smtp_object.starttls())
# user = User.query.filter_by(email=email).first()    #   .first() Shows 1st result

print({{user.email}})