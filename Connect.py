import sys
import os
import time
import hmac
import hashlib
import struct
import getpass


PASSWORDS_FILE = "Passwords.txt"
INTERVAL = 15


def generate_pin(username, password, time_step):
    key_material = f"{username}:{password}"
    key = hashlib.sha256(key_material.encode()).digest()
    msg = struct.pack(">Q", time_step)
    h = hmac.new(key, msg, hashlib.sha256).digest()
    offset = h[-1] & 0x0F
    code = struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF
    return code % 1000000





def load_passwords():
    users = {}
    if not os.path.exists(PASSWORDS_FILE):
        return users
    with open(PASSWORDS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":", 1)
            if len(parts) == 2:
                users[parts[0]] = parts[1]
    return users


def save_user(username, password):
    with open(PASSWORDS_FILE, "a") as f:
        f.write(f"{username}:{password}\n")


def register_new_user(username):
    check = False
    password1 = getpass.getpass("Enter new password: ")
    while check != True:
        if password1 == getpass.getpass("Confirm password: "):
            check = True
        else:
            print("Passwords do not match. Please try again.")
    save_user(username, password1)
    print(f"User '{username}' registered successfully.")


def authenticate_user(username, password, pin_str):
    users = load_passwords()
    stored_password = users[username]
    provided_pin = int(pin_str)
    now = time.time()
    current_step = int(now // INTERVAL)

    for step_offset in [-1, 0, 1]:
        expected_pin = generate_pin(username, password, current_step + step_offset)
        if provided_pin == expected_pin:
            print(f"Access granted. Welcome, {username}.")
            return

    print("Authentication failed.")
    sys.exit(1)


def main():
    if len(sys.argv) == 3 and sys.argv[2] == "new":
        register_new_user(sys.argv[1])
    elif len(sys.argv) == 4:
        authenticate_user(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage:")
        print("  Connect username new")
        print("  Connect username password pin")
        sys.exit(1)


if __name__ == "__main__":
    main()
