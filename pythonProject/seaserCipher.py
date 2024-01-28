import math
import random

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'e' to encrypt, type 'd' to decrypt:\n")
text = input("Type your message:\n").lower()
n_places = int(input("Type the shift number:\n"))


def encrypt(text_to_encrypt, num_places):
    encrypted_text = ""
    for ch in text_to_encrypt:
        total_move = (ord(ch)-ord("a"))+num_places
        # total_move = (int(ch) - int("a")) + num_places
        if total_move >= 26:
            new_ch = alphabet[total_move-25-1]
        else:
            new_ch = alphabet[total_move]
        encrypted_text += new_ch
    return encrypted_text


def decrypt(text_to_decrypt, num_places):
    decrypted_text = ""
    for ch in text_to_decrypt:
        if not ch.isalpha():
            print("invalid input- should be from a-z")
            return ""
        total_move = (ord(ch)-ord("a"))-num_places
        new_ch = alphabet[total_move]
        decrypted_text += new_ch
    return decrypted_text


encrypted = encrypt(text_to_encrypt=text, num_places=n_places)
decrypted = decrypt(text_to_decrypt=encrypted, num_places=n_places)
print(f"encrypted = {encrypted}")
print(f"decrypted = {decrypted}")
