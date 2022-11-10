import json
import os
import random


def key_generator() -> bytes:
    key:str = ""
    for i in range(0, 100):
        if i%4:
            key += chr(random.randint(0, 127))
        else:
            key += str(random.randint(0, 9))
    return key[:100].encode("UTF_8")

def decrypt_key(key: bytes) -> list:
    number:list = []
    key = key.decode("UTF_8")

    for i in range(len(key)):
        if i%4:
            number.append(ord(key[i]))
        else:
            if isinstance(key, int):
                number.append(key[i])
            else:
                number.append(ord(key[i]))
    
    return number

def encrypt_msg(msg:str, key:bytes) -> bytes:
    key:list = decrypt_key(key)
    password_encrypted:str = ""

    for i in range(len(msg)):
        password_encrypted += chr(ord(msg[i])+key[i])
    
    return password_encrypted.encode("UTF_8")

def decrypt_msg(encrypted_password:bytes, key:bytes) -> str:
    key:list = decrypt_key(key)
    encrypted_password = encrypted_password.decode("UTF_8")
    password:str = ""

    for i in range(len(encrypted_password)):
        password += chr(ord(encrypted_password[i])-key[i])
    
    return password

def combine_key_password(encrypted_password:bytes, key:bytes) -> bytes:
    encrypted_password = encrypted_password.decode("UTF_8")
    key = key.decode("UTF_8")

    encrytion = ""
    for i in range(len(encrypted_password)):
        encrytion += encrypted_password[i]
        encrytion += key[i]
    
    return encrytion.encode("UTF_8")

def decombine_key_password(encryption:bytes) -> tuple:
    encryption = encryption.decode("UTF_8")
    
    password: str = ""
    key: str = ""

    for i in range(len(encryption)):
        if i%2:
            password += encryption[i-1]
            key += encryption[i]
    
    return password.encode("UTF_8"), key.encode("UTF_8")

def encrypt_password(password:str) -> bytes:
    key = key_generator()
    encryted_password = encrypt_msg(password, key)
    encryption = combine_key_password(encryted_password, key)
    
    return encryption

def decrypt_password(encryption:bytes) -> str:
    en_password, key = decombine_key_password(encryption)    
    password = decrypt_msg(en_password, key)

    return password

def write_to_json(encryption:bytes, path:list):
    with open("brain.json", "r+") as file:
            data = json.load(file)

            if len(path) == 2:
                data["passwords"][path[0]].update({f"{path[1]}": encryption.decode("UTF_8")})
            elif len(path) == 1:
                data["passwords"].update({f"{path[0]}": encryption.decode("UTF_8")})
            else:
                return False
            
            file.seek(0)
            json.dump(data, file, indent=4)

def read_from_json() -> json:
    file = open(os.path.abspath("C:\\Users\\theod\\OneDrive\\Skrivebord\\Skript.Java\\python\\Voice Assistant\\version 1.0.1\\brain.json"), "r").read()
    jsonfile = json.loads(file)["passwords"]
    
    return jsonfile

if __name__ == '__main__':
    enpassword = encrypt_password("bertram0807")
    write_to_json(enpassword, ["lol", "eune2"])
