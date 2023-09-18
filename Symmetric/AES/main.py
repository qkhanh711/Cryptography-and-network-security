class AES:
    def __init__(self, key):
        self.key = key
        pass

    def add(self, block):
        pass
    
    def sub(self, block):
        pass

    def shift(self, block):
        pass

    def mix(self, block):
        pass

    def Block(self, block):
        pass

    def encrypt(self, plain):
        pass

    def decrypt(self, cipher):
        pass

    def key_expansion(self, key):
        pass

from AES import ENCRYPT, DECRYPT


import time
import argparse

parser = argparse.ArgumentParser(description='AES Encryption and Decryption')
parser.add_argument('-p', '--plaintext', default= "0123456789abcdeffedcba9876543210",type=str, help='Plain text')
parser.add_argument('-k', '--key', default="0f1571c947d9e8590cb7add6af7f6798", type=str, help='Cipher key')
parser.add_argument('-l', '--key_length', default = 176, type=int, help='Key length')
parser.add_argument('-r', '--print_rounds', default=False, type=bool, help='Print rounds')
args = parser.parse_args()

plaintext = args.plaintext
key = args.key
key_length = args.key_length
print_rounds = args.print_rounds


print("Plain text :", plaintext)
print("Cipher key :", key)
print("-----------------------------")
start = time.time()
ciphertext = ENCRYPT(plaintext, key, key_length=key_length, print_rounds=print_rounds)
end_encrypt = time.time()
print("Cipher text:", ciphertext)
print("-----------------------------")
print("Encryption time:", end_encrypt - start)
start_decrypt = time.time()
plaintext = DECRYPT(ciphertext, key, key_length=key_length, print_rounds=print_rounds)
print("Plain text :", plaintext)
end_decrypt = time.time()
print("Decryption time:", end_decrypt - start_decrypt)
print("-----------------------------")
