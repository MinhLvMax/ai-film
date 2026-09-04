import hashlib

password = "654321"

hashed = hashlib.sha256(password.encode()).hexdigest()

print(hashed)