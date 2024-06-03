import hashlib

# input both strings. they must be sha256, not sha512. 

def sha256_encode(data):
    return hashlib.sha256(data.encode()).hexdigest()

hashed_input = sha256_encode("2e4f21ab80da68522bedf85e285704820a3a0e1ba98970191c8ef1ffeee381a0b0b617a72cce1533572fc564bd42b3cd0f01ac7f1e4587c393fc9bed0f9c1273")

provided_hashed_result = "8a6c1f4a21e0e357699135b0c85dfc839f1aa61b7fcd482f3b19c09380b41624"

print("Hashed input:", hashed_input)
print("Provided hashed result:", provided_hashed_result)

if hashed_input == provided_hashed_result:
    print("Hashes match.")
else:
    print("Hashes do not match.")
