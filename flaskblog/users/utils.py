import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_picture.filename) # use underscores for variables you don't care about
  picture_fn = random_hex + f_ext # use hex to randomize same named images
  picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
  output_size = (125, 125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)
  # form_picture.save(picture_path) - discard because we are compressing images to 125 by 125 now

  return picture_fn

def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request', sender="pvanny1124@gmail.com", recipients=[user.email])
  msg.body = f'''
To Reset your password, vist the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request, then simply ignore this email and no changes will be made.
'''
  mail.send(msg)
