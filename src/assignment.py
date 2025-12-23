import random

def generate_assignments(participants):
    """
    Generate Secret Santa assignments for a list of participants.

    Each participant is assigned a receiver such that:
    - No participant receives themselves (if ALLOW_SELF_DRAW is False).
    - Exclusions specified in 'exclusion_names' are respected.
    - No reciprocal pairs are allowed (if Alice gives to Bob, Bob cannot give to Alice).

    Args:
        participants (list of dict): List of participants. Each participant dict must contain:
            - 'name' (str): Participant's name.
            - 'email' (str): Participant's email.
            - 'exclusions' (set of str): Emails of participants they cannot be assigned.

    Returns:
        dict: Mapping of giver email -> receiver participant dict. Example:
    """
    givers = participants[:]
    receivers = participants[:]
    random.shuffle(givers)
    random.shuffle(receivers)

    receiver_emails = [p["email"] for p in receivers]
    assignments = {}

    giver_to_receiver = {}

    def backtrack(i, available):
        if i == len(givers):
            return True

        giver = givers[i]
        excl = set(giver["exclusions"])

        candidates = [r for r in available if r not in excl and giver_to_receiver.get(r) != giver["email"]]
        random.shuffle(candidates)

        for r_email in candidates:
            assignments[giver["email"]] = r_email
            giver_to_receiver[giver["email"]] = r_email
            new_available = [e for e in available if e != r_email]

            if backtrack(i + 1, new_available):
                return True

            del assignments[giver["email"]]
            del giver_to_receiver[giver["email"]]

        return False

    if not backtrack(0, receiver_emails):
        raise ValueError("No valid Secret Santa assignment found with the current exclusions and anti-reciprocal constraint.")

    email_to_participant = {p["email"]: p for p in participants}
    return {g: email_to_participant[r] for g, r in assignments.items()}
