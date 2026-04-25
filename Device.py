import sys
import time
import hmac
import hashlib
import struct


def generate_pin(username, password, time_step):
    key_material = f"{username}:{password}"
    key = hashlib.sha256(key_material.encode()).digest()
    msg = struct.pack(">Q", time_step)
    h = hmac.new(key, msg, hashlib.sha256).digest()
    offset = h[-1] & 0x0F
    code = struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF
    return code % 1000000


def main():
    if len(sys.argv) != 3:
        print("Usage: Device username password")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    interval = 15
    last_step = None

    while True:
        now = time.time()
        current_step = int(now // interval)

        if current_step != last_step:
            pin = generate_pin(username, password, current_step)
            print(f"Device: {pin:06d}")
            last_step = current_step

        time.sleep(0.5)


if __name__ == "__main__":
    main()
