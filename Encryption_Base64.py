import base64
#Encryption
message = input("输入你要base加密的内容:\n")
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')
print("Base64加密结果为："+base64_message)

#Decryption
base64_bytes = base64_message.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
message = message_bytes.decode('ascii')

print("你加密的原内容是："+message)
