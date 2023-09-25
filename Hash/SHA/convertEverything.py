def string2hex(string):
    return string.encode('utf-8').hex()

def hex2string(hex):
    return bytearray.fromhex(hex).decode()

def string2bin(string):
    return bin(int(string2hex(string), 16))[2:]

def bin2string(bin):
    return hex2string(hex(int(bin, 2))[2:])

def hex2bin(hex):
    return bin(int(hex, 16))[2:]

def bin2hex(bin):
    return hex(int(bin, 2))[2:]

def hex2int(hex):
    return int(hex, 16)

def int2hex(int):
    return hex(int)[2:]