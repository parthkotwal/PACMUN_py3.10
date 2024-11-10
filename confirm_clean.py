import pandas as pd
import re

df = pd.read_excel("PACMUN2024AtConferenceMessagingPreferenceForm.xlsx")

def normalize_phone_number(phone):
    phone = re.sub(r'\D', '', phone)
    
    if len(phone) == 11 and phone.startswith('1'):
        return '+1' + phone[1:]
    elif len(phone) == 10:
        return '+1' + phone
    return phone

df['Phone Number'] = [normalize_phone_number(x) for x in df['PleaseInputYourPreferredPhoneNumber']]
df['FirstName'] = df['FirstName'].str.title()
df['LastName'] = df['LastName'].str.title()
df = df[df['YesNo'] == 'Yes']
df = df[['Phone Number','FirstName','LastName','Choice']]

print(df)
df.to_csv("PACMUN2024AtConferenceMessagingPreferenceForm.csv", index=False)

# REMOVE EVERYONE BEFORE Stephanie Breuker EXCEPT FOR ME AND TEST ALEMSHOWA!!
# REMOVE RAMIRU RAMASINGHA and MARLO DORNY
