from config import sbox, sboxInv, rcon

def rotate(word, n):
    return word[n:]+word[0:n]

def key_expansion(cipherKey):
    return cipherKey