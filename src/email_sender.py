import smtplib
from email.message import EmailMessage
from config.parameters import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SENDER_NAME, EMAIL_SUBJECT

def send_emails(participants, assignments):
    """
    Send Secret Santa emails to all participants.

    Each giver receives an email telling them who they should give a gift to.
    Both plain text and HTML versions of the email are sent.

    Args:
        participants (list of dict): List of participant dictionaries. Each dict contains:
            - 'name' (str): Participant's name
            - 'email' (str): Participant's email
            - 'exclusions' (set): Emails of participants to exclude (not used here)
        assignments (dict): Mapping of giver email -> receiver participant dict. Example:
            {
                'alice@example.com': {'name': 'Bob', 'email': 'bob@example.com', 'exclusions': {...}},
                ...
            }
    """
    email_to_participant = {p["email"]: p for p in participants}

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)

        for giver_email, receiver in assignments.items():
            giver = email_to_participant[giver_email]
            msg = EmailMessage()
            msg["From"] = f"{SENDER_NAME} <{SMTP_USER}>"
            msg["To"] = giver_email
            msg["Subject"] = EMAIL_SUBJECT

            text = (
                f"Ho ho ho, {giver['name']}! 🎅\n\n"
                f"This is Santa Claus speaking for the Secret Santa 🎄\n\n"
                f"The draw is done, and you will be giving a gift to: {receiver['name']} 🎁\n\n"
                f"The suggested budget is around 20CHF.\n"
                f"Shh 🤫… keep it a secret!\n\n"
                f"{SENDER_NAME}\n"
            )
            msg.set_content(text)

            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <p><b>Ho ho ho, {giver['name']}! 🎅</b></p>
                <p>This is Santa Claus speaking for the <b>Secret Santa</b> 🎄</p>
                <p>The draw is done, and you will be giving a gift to:<br/>
                   <b style="font-size: 1.2em;">{receiver['name']}</b> 🎁</p>
                <p><b>Budget: around 20CHF</b></p>
                <p>Shh 🤫… keep it a secret!</p>
                <p>{SENDER_NAME}</p>
            </body>
            </html>
            """
            msg.add_alternative(html, subtype="html")
            server.send_message(msg)
