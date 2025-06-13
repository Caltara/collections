def send_voice(to, name, amount, due_date):
    twiml = f"""
    <Response>
        <Gather numDigits="1" action="/handle-key" method="POST" timeout="6">
            <Say voice="alice" language="en-US">
                Hi {name}, this is Caltara with a quick reminder.
                <Pause length="1"/>
                You have a past due balance of {amount} dollars due on {due_date}.
                <Pause length="1"/>
                If you’d like to speak with someone now to resolve your balance, please press 1.
                <Pause length="1"/>
                Or, you can visit your invoice link online at your convenience.
                <Pause length="1"/>
                Thank you for your time, and have a great day!
            </Say>
        </Gather>
        <Say voice="alice" language="en-US">
            We didn’t catch any input. Goodbye for now!
        </Say>
    </Response>
    """
    call = client.calls.create(
        twiml=twiml,
        to=to,
        from_=TWILIO_PHONE
    )
    return call
