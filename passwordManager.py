import hashlib
import os
import hmac
def validatePassword(password):
    if len(password) < 8:
        return "Password must contain at least 8 characters."

    if not any(c.isupper() for c in password):
        return "Password must contain an uppercase letter."

    if not any(c.islower() for c in password):
        return "Password must contain a lowercase letter."

    if not any(c.isdigit() for c in password):
        return "Password must contain a number."

    if not any(not c.isalnum() and not c.isspace() for c in password):
        return "Password must contain a special character."

    return None
def hashPassword(password):
    salt = os.urandom(16) #random bits generated stored in salt for the 1st value for the hashed password

    hashedPassword = hashlib.scrypt(    #hashing the password
        password.encode(),
        salt=salt,
        n=2**17, #CPU and memory
        r=8,    #block size 
        p=1, #parallelisation parameter
        maxmem=256 * 1024 * 1024    #max memory used
    )

    return salt.hex() + ":" + hashedPassword.hex()  #returns hashed password


def verifyPassword(storedHash, password):
    try:
        salt, hashedPassword = storedHash.split(":")

        newHash = hashlib.scrypt(
            password.encode(),
            salt=bytes.fromhex(salt),
            n=2**17,
            r=8,
            p=1,
            maxmem=256 * 1024 * 1024
        )

        return hmac.compare_digest(newHash.hex(), hashedPassword)   #compares whether the password being hashed is in the database

    except (ValueError, AttributeError):
        return False