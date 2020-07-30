import base64
encoded_data = base64.b64encode(b"192.168.123.112")

print("Encoded text with base 64 is")
print(encoded_data ,len(encoded_data))

decoded_data = base64.b64decode(encoded_data)
print(decoded_data)



from Crypto.Cipher import AES

msg_text = b'192.168.1.100'.rjust(32)
secret_key = b'1234567890123456'

cipher = AES.new(secret_key,AES.MODE_ECB) # never use ECB in strong systems obviously
print("\n\nUsing AES cipher")
encoded = base64.b64encode(cipher.encrypt(msg_text))
print(encoded)
decoded = cipher.decrypt(base64.b64decode(encoded))
print(decoded)

