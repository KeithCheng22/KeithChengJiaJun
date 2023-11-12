from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import smtplib
import os

MY_EMAIL = 'keithcheng.jj@gmail.com'
PASSWORD = os.environ.get('PASSWORD')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
Bootstrap5(app)


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField("Let's Connect!")

# Send contact details to my email
def contact_info(name, email, message):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user='keithcheng.sgs@gmail.com', password=PASSWORD)
        connection.sendmail(from_addr='keithcheng.sgs@gmail.com', to_addrs=MY_EMAIL, msg=f'Subject: New Query!\n\nName: {name}\nEmail: {email}\nMessage: {message}' )


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact-me', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # Send contact details to my email
        contact_info(name, email, message)

        form.name.data = ""
        form.email.data = ""
        form.message.data = ""
        return render_template('contact.html', form=form, submitted=True)
    return render_template('contact.html', form=form)

@app.route('/projects')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(debug=True)
