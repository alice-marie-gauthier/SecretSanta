import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ==============================
# SMTP CONFIG
# ==============================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_NAME = "Secret Santa Organizer"
EMAIL_SUBJECT = "🎄 Secret Santa Draw"

# ==============================
# OPTIONS
# ==============================
ALLOW_SELF_DRAW = False

# ==============================
# PARTICIPANTS
# ==============================
RAW_PARTICIPANTS = []

for key, value in os.environ.items():
    if key.startswith("PARTICIPANT_"):
        parts = [p.strip() for p in value.split(",")]
        if len(parts) < 2:
            raise ValueError(f"Invalid participant format for {key}: {value}")

        name = parts[0]
        email = parts[1]
        exclusions = parts[2:] if len(parts) > 2 else []

        RAW_PARTICIPANTS.append({
            "name": name,
            "email": email,
            "exclusion_names": exclusions
        })

# ==============================
# CHECK PARTICIPANT COUNT
# ==============================
MIN_PARTICIPANTS = 3
if len(RAW_PARTICIPANTS) < MIN_PARTICIPANTS:
    raise ValueError(f"Secret Santa requires at least {MIN_PARTICIPANTS} participants. Currently: {len(RAW_PARTICIPANTS)}")
