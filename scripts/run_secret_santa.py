import sys
import os
from config.parameters import RAW_PARTICIPANTS
from src.participants import build_participants
from src.assignment import generate_assignments
from src.email_sender import send_emails

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    """
    Main function to run the Secret Santa draw.

    Steps:
        1. Build validated participants from RAW_PARTICIPANTS.
        2. Generate assignments respecting exclusions and anti-reciprocal constraints.
        3. Print results to the console (for debugging).
        4. Prompt the user to confirm sending emails.
        5. Send emails to participants if confirmed.
    """
    participants = build_participants(RAW_PARTICIPANTS)
    assignments = generate_assignments(participants)

    print("\n=== DRAW RESULT (DEBUG) ===")
    for giver_email, receiver in assignments.items():
        giver_name = next(p["name"] for p in participants if p["email"] == giver_email)
        print(f"{giver_name} -> {receiver['name']}")

    confirm = input("\nSend emails now? (y/n): ").strip().lower()
    if confirm == "y":
        send_emails(participants, assignments)
        print("✅ Emails sent.")
    else:
        print("⛔ Cancelled. No email was sent.")

if __name__ == "__main__":
    main()
