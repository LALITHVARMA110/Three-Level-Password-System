import time
import getpass
import hashlib
import random
import string
import pyotp

# Sample user database with OTP secrets
users_db = {
    "user1": {
        "password_hash": hashlib.sha256("ComplexP@ssw0rd!123".encode()).hexdigest(),
        "graphical_password": ["img2", "img5", "img8"],  # Click sequence on images
        "otp_secret": pyotp.random_base32()  # Generate a new OTP secret
    }
}

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password_strength(password):
    """Checks password strength based on length and character variety."""
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in string.punctuation for char in password):
        return False
    return True

def authenticate_password(username, password):
    """Level 1: Authenticate with a textual password."""
    if not check_password_strength(password):
        print("Password is not strong enough.")
        return False
    stored_hash = users_db.get(username, {}).get("password_hash")
    return stored_hash == hash_password(password)

def authenticate_graphical_password(username):
    """Level 2: Authenticate with a graphical password."""
    stored_sequence = users_db[username]["graphical_password"]
    available_images = [f"img{i}" for i in range(1, 10)]  # Assume a set of 9 images

    print("Click on the following images in sequence:")
    selected_sequence = [input(f"Click image (1-9): ") for _ in range(len(stored_sequence))]
    return selected_sequence == stored_sequence

def generate_otp(username):
    """Generates and returns an OTP for the user."""
    otp_secret = users_db[username]["otp_secret"]
    totp = pyotp.TOTP(otp_secret)
    return totp.now()

def authenticate_otp(username):
    """Level 3: Authenticate using OTP."""
    otp_secret = users_db[username]["otp_secret"]
    totp = pyotp.TOTP(otp_secret)

    # Generate and display OTP
    generated_otp = generate_otp(username)
    print(f"Your OTP is: {generated_otp}")

    # Simulate sending OTP to user
    input("Enter the OTP received: ")

    # Validate entered OTP
    user_otp = input("Enter the OTP: ")
    if totp.verify(user_otp):
        print("OTP authentication successful.")
        return True
    else:
        print("OTP authentication failed.")
        return False

def main():
    username = input("Enter your username: ")

    if username not in users_db:
        print("User does not exist.")
        return

    # Level 1: Textual Password Authentication
    password = getpass.getpass("Enter your password: ")
    if not authenticate_password(username, password):
        print("Password authentication failed.")
        return

    # Level 2: Graphical Password Authentication
    if not authenticate_graphical_password(username):
        print("Graphical password authentication failed.")
        return

    # Level 3: OTP Authentication
    if not authenticate_otp(username):
        print("OTP authentication failed.")
        return

    print("Three-Level Password System authentication successful. Access granted.")

if __name__ == "__main__":
    main()
