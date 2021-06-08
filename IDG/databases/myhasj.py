import hashlib

mk = hashlib.pbkdf2_hmac('sha512', b'Joakim', b'salt', 100_000)
dk = hashlib.pbkdf2_hmac('sha512', b'Joakim', b'salt', 100_000)
print(dk.hex() == mk.hex())
