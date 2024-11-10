import pandas as pd
from twilio.rest import Client
import os

# Twilio configuration
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = '+18333250753'
client = Client(account_sid, auth_token)

personalized_message = "Hey Uzhair! Here is a kind and sweet message."
client.messages.create(
    body=personalized_message,
    from_=twilio_number,
    to="+12066762348"
)