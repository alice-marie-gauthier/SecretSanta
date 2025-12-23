from config.parameters import ALLOW_SELF_DRAW

def build_participants(raw):
    """
    Build and validate participants for Secret Santa.

    This function:
        - Ensures all emails are unique.
        - Converts participant exclusions from names to emails.
        - Optionally adds self-exclusion if ALLOW_SELF_DRAW is False.
        - Raises errors if exclusions reference unknown participants.

    Args:
        raw (list of dict): List of raw participant dictionaries. Each dictionary should contain:
            - 'name' (str): Participant's name
            - 'email' (str): Participant's email
            - 'exclusion_names' (list of str, optional): List of names this participant cannot be assigned to

    Returns:
        list of dict: Validated participants with the following keys:
            - 'name' (str)
            - 'email' (str)
            - 'exclusions' (set of str): Set of emails the participant cannot be assigned
    """
    emails = [p["email"].strip().lower() for p in raw]
    if len(emails) != len(set(emails)):
        raise ValueError("Duplicate email detected. Each participant must have a unique email.")

    name_to_email = {p["name"].strip().lower(): p["email"].strip().lower() for p in raw}
    known_names = set(name_to_email.keys())

    participants = []
    for p in raw:
        name = p["name"].strip()
        email = p["email"].strip().lower()

        exclusion_names = [n.strip() for n in p.get("exclusion_names", []) if n.strip()]
        unknown = [n for n in exclusion_names if n.lower() not in known_names]
        if unknown:
            raise ValueError(f"Unknown exclusion name for {name}: {unknown}")

        exclusions_emails = {name_to_email[n.lower()] for n in exclusion_names}

        if not ALLOW_SELF_DRAW:
            exclusions_emails.add(email)

        participants.append({"name": name, "email": email, "exclusions": exclusions_emails})

    return participants
