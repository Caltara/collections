from twilio.rest import Client
import streamlit as st

TWILIO_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = st.secrets["TWILIO_PHONE_NUMBER"]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_sms(to, name, amount, due_date):
    message = f"Hi {name}, this is a friendly reminder from Caltara. You have an unpaid invoice of ${amount} due on {due_date}. Please reply or call to arrange payment."
    return client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=to
    )

def send_voice(to, name, amount, due_date, domain_url):
    call = client.calls.create(
        url=f"{domain_url}/voice?name={name}&amount={amount}&due={due_date}",
        to=to,
        from_=TWILIO_PHONE
    )
    return call
