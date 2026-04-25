Two-Factor Authentication Simulation
=====================================

Pin Generation Algorithm and Security Explanation
--------------------------------------------------

The relationship between Device and Connect:

Both programs derive a shared secret key by computing the SHA-256 hash of the string "username:password". They then use an HMAC-SHA256 construction over a time step value, where the time step is the current Unix time divided by 15 (integer division), so it changes every 15 seconds. A 6-digit pin is extracted from the HMAC output using a truncation method modelled on RFC 6238 (TOTP).

Because both Device and Connect use the same username, password, and system clock, they independently produce identical pin values for the same 15-second window without any communication between them.

Why pins do not leak information about the password:

1. The key is derived via SHA-256, a one-way cryptographic hash function. Given the key or the HMAC output, it is computationally infeasible to reverse the hash to recover the original password.

2. Each pin is a 6-digit integer extracted from the HMAC output by truncation. The truncation discards the majority of the HMAC bits, making it impossible to reconstruct the full HMAC value from the pin alone.

3. Because the time step changes every 15 seconds, each pin is unique to that window. An attacker who observes a pin gains no useful information about the password, and the pin cannot be reused in a later window.

4. The HMAC construction ensures that even small changes to the username or password produce entirely different pin sequences due to the avalanche effect of SHA-256.

Important!!
--------------
There is no validation as per the questions request. Connect.py will break if the password and username seperator (:) is used in either the password or username. This will result in a key error!!!

Files Included
--------------
Device.py   - Generates time-based one-time pins for a given user and password.
Connect.py  - Registers new users or authenticates existing users using username, password, and pin.
Readme.txt  - This file.


Requirements
------------
Python 3.6 or higher.
No external libraries are required. All modules used (sys, os, time, hmac, hashlib, struct, getpass) are part of the Python standard library.


How to Run
----------

Device:

    python3 Device.py <username> <password>

    Example:
        python3 Device.py Alice 1wdcasFga

    Device will begin printing a 6-digit one-time pin immediately. Every 15 seconds a new pin is printed. The program runs until interrupted with Ctrl-C.


Connect (new user registration):

    python3 Connect.py <username> new

    Example:
        python3 Connect.py Alice new

    You will be prompted to enter and confirm a password. The password must:
      - Be at least 8 characters long
      - Contain at least one uppercase letter
      - Contain at least one lowercase letter
      - Contain at least one digit

    On success, the user and password are stored in plain text in Passwords.txt in the format:
        username:password


Connect (authentication):

    python3 Connect.py <username> <password> <pin>

    Example:
        python3 Connect.py Alice 1wdcasFga 837226

    Connect reads Passwords.txt to verify the username and password, then verifies the pin using the same time-based algorithm as Device. The pin is accepted if it matches the current 15-second window, or the immediately preceding or following window, to account for clock skew between machines.


Passwords.txt
-------------
This file is created automatically by Connect in the same directory from which Connect is run. It stores credentials in plain text as required by the assignment. It is not encrypted and should not be used in production systems.


