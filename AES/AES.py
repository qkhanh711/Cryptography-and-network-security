from utils import *
from config import *

################################# ENCRYPTOR ################################################

def EncryptBlock(state, roundKeys, crypt = "encrypt", print_rounds = False):
    if print_rounds:
        print("                               Initial transformation: ")
    roundKeyIndex = 0
    if print_rounds:
        print("    After subtitute byte:", None)
        print("    After mixColumns byte:", None)
        print("    After shift rows byte:", None)
    added_state = add_round_key(state, roundKeys[:16], print_round_key=False)
    if print_rounds:
        print("    After add round key byte: ",)
        visualize(added_state)
    for round in range(1, len(roundKeys) // 16 - 1):
        if print_rounds:
            print("                               Round", round)
        sub_state = substitute_bytes(added_state, crypt=crypt)
        sub_state = [int(element, 16) for element in sub_state]
        if print_rounds:
            print("    After subtitute byte")
            visualize(sub_state)
        shift_state = shift_rows(sub_state, crypt=crypt)
        if print_rounds:
            print("    After shift rows byte")
            visualize(shift_state)
        mix_state = mixColumns(shift_state, crypt=crypt)
        if print_rounds:
            print("    After mixColumns byte")
            visualize(mix_state)
        if crypt == "encrypt":
            added_state = add_round_key(mix_state, roundKeys[roundKeyIndex + 16:roundKeyIndex + 32], print_round_key=False)
        else:
            added_state = add_round_key(mix_state, roundKeys[len(roundKeys) - roundKeyIndex - 32:len(roundKeys) - roundKeyIndex - 16], print_round_key=False)
        if print_rounds:
            print("    After add round key byte")
            visualize(added_state)
          
        roundKeyIndex += 16
    if print_rounds:
        print("                               Last round")
    sub_state = substitute_bytes(added_state, crypt=crypt)
    sub_state = [int(element, 16) for element in sub_state]
    if print_rounds:
        print("    After subtitute byte")
        visualize(sub_state)
    shift_state = shift_rows(sub_state, crypt=crypt)
    if print_rounds:
        print("    After shift rows byte")
        visualize(shift_state)  
    state = add_round_key(shift_state, roundKeys[(len(roundKeys)-16):], print_round_key=False)
    if print_rounds:
        print("    After add round key byte")
        visualize(state)
    # Chuyển đổi trạng thái trở lại dạng hex
    state = [format(byte, '02x') for byte in state]
    
    return transpose(state)

def ENCRYPT(plaintext, cipherKey, key_length=240, print_rounds = False):
    if print_rounds:
        print("Start of Round:")
        visualize(char_to_hex(plaintext, option="int value"))
    state = char_to_hex(plaintext, option="int value")
    cipherKey = char_to_hex(cipherKey, option="int value", key=True)
    expandedKey = expandKey(cipherKey, key_length)
    ciphertext = []

    state = EncryptBlock(state, expandedKey, crypt="encrypt", print_rounds=print_rounds)
    ciphertext.extend(state)

    return "".join(ciphertext)

################################# DECRYPTOR ################################################
def DecryptBlock(state, roundKeys, crypt = "encrypt", print_rounds = False):
    if print_rounds:
        print("                               Initial transformation: ")
    roundKeyIndex = 0
    if print_rounds:
        print("    After subtitute byte:", None)
        print("    After mixColumns byte:", None)
        print("    After shift rows byte:", None)
    added_state = add_round_key(state, roundKeys[(len(roundKeys)-16):], print_round_key=False)
    if print_rounds:
        print("    After add round key byte: ",)
        visualize(added_state)
    for round in range(1, len(roundKeys) // 16 - 1):
        if print_rounds:
            print("                               Round", round)
        shift_state = shift_rows(added_state, crypt=crypt)
        if print_rounds:
            print("    After shift rows byte")
            visualize(shift_state)
        sub_state = substitute_bytes(shift_state, crypt=crypt)
        sub_state = [int(element, 16) for element in sub_state]
        if print_rounds:
            print("    After subtitute byte")
            visualize(sub_state)
        added_state = add_round_key(sub_state, roundKeys[len(roundKeys) - roundKeyIndex - 32:len(roundKeys) - roundKeyIndex - 16], print_round_key=False)
        if print_rounds:
            print("    After add round key byte")
            visualize(added_state)
        mix_state = mixColumns(added_state, crypt=crypt)
        if print_rounds:
            print("    After mixColumns byte")
            visualize(mix_state)
        roundKeyIndex += 16
    if print_rounds:
        print("                               Last round")

    shift_state = shift_rows(mix_state, crypt=crypt)
    if print_rounds:
        print("    After shift rows byte")
        visualize(shift_state)  
    sub_state = substitute_bytes(shift_state, crypt=crypt)
    sub_state = [int(element, 16) for element in sub_state]
    if print_rounds:
        print("    After subtitute byte")
        visualize(sub_state)
    state = add_round_key(sub_state, roundKeys[:16], print_round_key=False)
    if print_rounds:
        print("    After add round key byte")
        visualize(state)
    state = [format(byte, '02x') for byte in state]
    
    return transpose(state)

def DECRYPT(ciphertext, cipherKey, key_length=240, print_rounds = False):
    if print_rounds:
        print("Start of Round:")
        visualize(char_to_hex(ciphertext, option="int value"))
    state = char_to_hex(ciphertext, option="int value")
    # print ("Cipherkey: ")
    # visualize(char_to_hex(cipherKey, option="int value"))
    cipherKey = char_to_hex(cipherKey, option="int value", key=True)
    expandedKey = expandKey(cipherKey, key_length)
    plaintext = []

    state = DecryptBlock(state, expandedKey, crypt="decrypt", print_rounds=print_rounds)
    plaintext.extend(state)

    return "".join(plaintext)