from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
from twilio.rest import Client
import os

app = Flask(__name__)
app.secret_key = "c07baf923f2d9a23142b725d"

# Twilio configuration
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = '+18333250753'
client = Client(account_sid, auth_token)

delegates_df = pd.read_csv('data/delegates.csv',dtype={'Phone Number': str})
staff_df = pd.read_csv('data/staff.csv',dtype={'Phone Number': str})
advisors_df = pd.read_csv('data/advisors.csv',dtype={'Phone Number': str})
secretariat_df = pd.read_csv('data/secretariat.csv',dtype={'Phone Number': str})

datasets = {
    'Delegates': delegates_df,
    'Staff': staff_df,
    'Advisors': advisors_df,
    'Secretariat': secretariat_df
}

# new
import re
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_sms',methods=['GET','POST'])
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
    app.run(debug=True)