# Secret Santa Organizer

Automated Python tool to manage Secret Santa gift assignments and send emails to participants.

## Features
- Configurable participants, exclusions, and SMTP settings
- Random assignment with backtracking to satisfy exclusions
- Optional prevention of self-assignment
- Sends personalized emails with HTML formatting

## Usage

1. Edit `config/parameters.py` for participants and email settings.
2. Run the main script:

```bash
python -m scripts/run_secret_santa
