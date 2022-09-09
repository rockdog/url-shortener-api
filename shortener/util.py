import secrets
import string

MAX_LENGTH = 256


def generate_random_key(length: int = 5) -> str:
    assert length <= MAX_LENGTH, f"limit must be smaller or equal than {MAX_LENGTH}"
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))
