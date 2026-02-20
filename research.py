import hashlib

# 1. Encode string to bytes
data = "example_text".encode()

# 2. Create hash object and update it
hash_object = hashlib.sha256(data)

# 3. Get the hexadecimal representation
print(hash_object.hexdigest()) 
# Output: 56641e7790850...
