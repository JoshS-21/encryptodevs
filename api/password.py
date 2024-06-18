import re

def validate_password(password):
    if len(password) < 7:
        return False, "Password must be at least 7 characters long"
    if not re.search(r"[!£$%_-]", password):
        return False, "Password must contain at least one special character (!£$%_-)"
    return True, ""

