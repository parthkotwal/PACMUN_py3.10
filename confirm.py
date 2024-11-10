import pandas as pd
from twilio.rest import Client
import os

# Twilio configuration
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = '+18333250753'
client = Client(account_sid, auth_token)

df = pd.read_csv('PACMUN2024AtConferenceMessagingPreferenceForm.csv', dtype={'Phone Number': str})

# personalized_message = f"""
# Hello {me['FirstName'].values[0]}! This is a message to confirm your preference to opt into PACMUN 2024's at-conference messaging system. We look forward to having you at PACMUN as a {me['Choice'].values[0].lower()} on November 23rd, 2024!
# """
# client.messages.create(
#     body=personalized_message,
#     from_=twilio_number,
#     to=me['Phone Number'].values[0]
# )

for index, row in df.iterrows():
    personalized_message = f"""
Hello {row['FirstName']}! This is a message to confirm your preference to opt into PACMUN 2024's at-conference messaging system. We look forward to having you at PACMUN as a {row['Choice'].lower()} on November 23rd, 2024!
    """
    client.messages.create(
        body=personalized_message,
        from_=twilio_number,
        to=row['Phone Number']
    )