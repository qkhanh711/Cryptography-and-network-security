from mpmath import *
import sympy as s
from convertEverything import *
# 2. Preprocessing message

def convert_to_bin(message):
    message = message.encode('utf-8')
    message = message.hex()
    message = bin(int(message, 16))
    message = message[2:]
    return '0' + message

def convert_to_hex(message):
    message = message.encode('utf-8')
    message = message.hex()
    return message

# 3 Padding message
def add_padding(message, N, option = 'hex'):
    L = len(convert_to_bin(message))
    if option == 'hex':
        message = convert_to_hex(message)
        message = message + '80' + '0' * (N * 256 - 32 - 2 - len(message)) + hex(L)[2:].zfill(32)
    else:
        message = convert_to_bin(message)
        message += '1' + '0' * (N * 1024 - 128 - L - 1) + bin(L)[2:].zfill(128)
    return message

def sqrt_64bits_hex(n): # the 64-bit of the fractional part of the square root
    return (hex(int(fmul(frac(sqrt(n)), pow(2, 64))))[2:])