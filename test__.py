def encode(msg):
    encoded_msg=''
        
    for i in msg:            # use the built-in method ord()and chr() 
            # to convert letters into digits and mess up the original message
        encoded_msg+=chr(ord(i)+5)
    return encoded_msg

def decode(encoded_msg):
    decoded_msg=''
    for i in encoded_msg:
         # the reversed operation of encode
        decoded_msg+=chr(ord(i)-5)
    return decoded_msg

msg="Hi"
print(encode(msg))
print(decode(msg))