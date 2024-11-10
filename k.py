from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from twilio.rest import Client
import os
import re

app = Flask(__name__)
app.secret_key = "c07baf923f2d9a23142b725d"

# Twilio configuration
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = '+18333250753'
client = Client(account_sid, auth_token)

# Setting file paths to datasets
basedir = os.path.abspath(os.path.dirname(__file__))
delegates_file = os.path.join(basedir, 'data', 'delegates.csv')
staff_file = os.path.join(basedir, 'data', 'staff.csv')
advisors_file = os.path.join(basedir, 'data', 'advisors.csv')
secretariat_file = os.path.join(basedir, 'data', 'secretariat.csv')

# Extracting data as dataframes
delegates_df = pd.read_csv(delegates_file, dtype={'Phone Number': str})
staff_df = pd.read_csv(staff_file, dtype={'Phone Number': str})
advisors_df = pd.read_csv(advisors_file, dtype={'Phone Number': str})
secretariat_df = pd.read_csv(secretariat_file, dtype={'Phone Number': str})

datasets = {
    'Delegates': delegates_df,
    'Staff': staff_df,
    'Advisors': advisors_df,
    'Secretariat': secretariat_df
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Predefined user passwords (hashed)
users = {
    'BETSY': generate_password_hash('betsythefish'),
    'RAIKA': generate_password_hash('raikathebird'),
    'AISHA': generate_password_hash('aishathedog'),
    'ERIC': generate_password_hash('ericthemonkey'),
    'MISHA': generate_password_hash('mishathebug'),
    'CHEN': generate_password_hash('chenthegoat'),
    'GWEN': generate_password_hash('gwenthecat'),
    'PARTH': generate_password_hash('parththepig'),
    'ALEX': generate_password_hash('alexthecow'),
    'MADDIE': generate_password_hash('maddiethebear'),
    'CHARLIE': generate_password_hash('charliethekangaroo'),
    'PRIYOSHI': generate_password_hash('priyoshithechicken'),
    'LIAM': generate_password_hash('liamtherat'),
    'MINA': generate_password_hash('minathepenguin')
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.id)

def personalize_message(message, row):
    """
    Replace placeholders in the message with actual data from the row.
    Placeholders are in the format {{Column Name}}.
    """
    placeholders = re.findall(r'{{(.*?)}}', message)
    for placeholder in placeholders:
        if placeholder in row:
            # Replace the placeholder with the actual value from the row
            message = message.replace(f'{{{{{placeholder}}}}}', str(row[placeholder]))
    return message

@app.route('/send_sms',methods=['GET','POST'])
@login_required
def send_sms():
    message_template = request.form['message']
    selected_groups = request.form.getlist('groups')
    selected_secretariat_members = request.form.getlist('secretariat_members')
    print(f"Selected Groups: {selected_groups}")  # Debugging
    print(f"Selected Secretariat Members: {selected_secretariat_members}")  # Debugging
    recipients = []

    for group in selected_groups:
        if group == 'Secretariat' and selected_secretariat_members:
            secretariat_df = datasets['Secretariat']
            secretariat_members = secretariat_df[secretariat_df['First Name'].isin([name.split(' ')[0] for name in selected_secretariat_members])]
            for _, row in secretariat_members.iterrows():
                personalized_message = personalize_message(message_template, row)
                recipients.append((row['Phone Number'], personalized_message))
        else:
            df = datasets.get(group, pd.DataFrame())
            for _, row in df.iterrows():
                personalized_message = personalize_message(message_template, row)
                recipients.append((row['Phone Number'], personalized_message))

    for recipient, personalized_message in recipients:
        try:
            client.messages.create(
                body=personalized_message,
                from_=twilio_number,
                to=recipient
            )
        except Exception as e:
            flash(f'Error sending message to {recipient}: {e}', 'danger')
            continue

    flash('Messages sent successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()