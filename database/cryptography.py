import hashlib

#Dla uproszczenia wszyscy używają tej samej soli
SALT = 'K0ef4wLme@xe'

def hash_password(password: str, salt: str = SALT) -> str:
    salted_password = password.encode() + salt.encode()
    return hashlib.sha256(salted_password).hexdigest()

def verify_password(provided_password: str, hashed_password: str, salt: str = SALT) -> bool:
    computed_hash = hash_password(provided_password, salt)
    return computed_hash == hashed_password
