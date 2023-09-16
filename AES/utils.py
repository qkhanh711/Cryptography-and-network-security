from config import sbox, sboxInv, rcon

def visualize(matrix):
    for i in range(4):
        print(" ".join([f"{matrix[i*4+j]:02x}" for j in range(4)]))

def transpose(hex_state):
    hex_matrix = [hex_state[i:i+4] for i in range(0, 16, 4)]
    transposed_hex_matrix = [[row[i] for row in hex_matrix] for i in range(4)]
    return [item for sublist in transposed_hex_matrix for item in sublist]

def char_to_hex(plaintext, option="char", key = False):
    if option == "char":
        if key:
            return [plaintext[i:i + 2] for i in range(0, len(plaintext), 2)]
        hex_state = [plaintext[i:i + 2] for i in range(0, len(plaintext), 2)]
        return transpose(hex_state)
    elif option == "int value":
        if key:
            return [int(plaintext[i:i + 2], 16) for i in range(0, len(plaintext), 2)]
        int_state = [int(plaintext[i:i + 2], 16) for i in range(0, len(plaintext), 2)]
        int_matrix = [int_state[i:i+4] for i in range(0, 16, 4)]
        transposed_int_matrix = [[row[i] for row in int_matrix] for i in range(4)]
        return [item for sublist in transposed_int_matrix for item in sublist]
    else:
        print("Invalid option. Please choose 'char' or 'int value'.")

def hex_to_char(hex_state, key = False):
    if key:
        new = hex_state
    else:
        new = transpose(hex_state)
    char_string = "".join(new)
    return char_string

################################# KEY SCHEDULE ################################################
def keyScheduleCore(word, i):
    word = rotate(word, 1)
    newWord = []
    for byte in word:
        newWord.append(sbox[byte])
    newWord[0] = newWord[0] ^ rcon[i]
    return newWord

def expandKey(cipherKey, key_length = 176):
    if key_length != 176 and key_length != 208 and key_length != 240:
        print("Invalid key length. Please choose 176, 208 or 240.")
    else:
        print("Encrytion start with key length: ", key_length, "bits <=> ", key_length // 16, "rounds")
        expandedKey = list(cipherKey) 
        currentSize = len(cipherKey)
        rconIter = 1
        t = [0, 0, 0, 0]
        while currentSize < key_length:
            for i in range(4):
                t[i] = expandedKey[currentSize - 4 + i]
            if currentSize % len(cipherKey) == 0:
                t = keyScheduleCore(t, rconIter)
                rconIter += 1
            for i in range(4):
                expandedKey.append(expandedKey[currentSize - len(cipherKey)] ^ t[i])
                currentSize += 1
        return expandedKey

################################# SUBBYTES ################################################
def substitute_bytes(state, crypt = "encrypt"):
    result_hex = []
    for byte_hex in state:
        # byte_int = int(byte_hex, 16)
        if crypt == "encrypt":
            substituted_byte = sbox[byte_hex]
        elif crypt == "decrypt": 
            substituted_byte = sboxInv[byte_hex]
        else:
            print("Invalid value! Crypt must be encrypt or decrypt")
        result_hex.append(format(substituted_byte, '02x'))  
    return result_hex

################################# SHIFT ROWS ################################################
def rotate(word, n):
    return word[n:]+word[0:n]

def shift_rows(state, crypt = "encrypt"):
    if crypt == "encrypt":
        for i in range(4):
            state[i*4:i*4+4] = rotate(state[i*4:i*4+4],i)
    elif crypt == "decrypt":
        for i in range(4):
            state[i*4:i*4+4] = rotate(state[i*4:i*4+4],-i)
    else:
        print("Invalid value! Crypt must be encrypt or decrypt")
    return state
################################# MIX COLUMNS ################################################
def galoisMult(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256

def mixColumn(column, crypt="encrypt"):
    if crypt == "encrypt":
        temp = column.copy()
        column[0] = galoisMult(temp[0], 2) ^ galoisMult(temp[3], 1) ^ galoisMult(temp[2], 1) ^ galoisMult(temp[1], 3)
        column[1] = galoisMult(temp[1], 2) ^ galoisMult(temp[0], 1) ^ galoisMult(temp[3], 1) ^ galoisMult(temp[2], 3)
        column[2] = galoisMult(temp[2], 2) ^ galoisMult(temp[1], 1) ^ galoisMult(temp[0], 1) ^ galoisMult(temp[3], 3)
        column[3] = galoisMult(temp[3], 2) ^ galoisMult(temp[2], 1) ^ galoisMult(temp[1], 1) ^ galoisMult(temp[0], 3)
    elif crypt == "decrypt":
        temp = column.copy()
        column[0] = galoisMult(temp[0], 14) ^ galoisMult(temp[3], 9) ^ galoisMult(temp[2], 13) ^ galoisMult(temp[1], 11)
        column[1] = galoisMult(temp[1], 14) ^ galoisMult(temp[0], 9) ^ galoisMult(temp[3], 13) ^ galoisMult(temp[2], 11)
        column[2] = galoisMult(temp[2], 14) ^ galoisMult(temp[1], 9) ^ galoisMult(temp[0], 13) ^ galoisMult(temp[3], 11)
        column[3] = galoisMult(temp[3], 14) ^ galoisMult(temp[2], 9) ^ galoisMult(temp[1], 13) ^ galoisMult(temp[0], 11)
    else:
        print("Invalid value! Crypt must be encrypt or decrypt")

def mixColumns(state, crypt="encrypt"):
    for i in range(4):
        column = []
        for j in range(4):
            column.append(state[j * 4 + i])
        mixColumn(column, crypt=crypt)
        # Transfer the new values back into the state table
        for j in range(4):
            state[j * 4 + i] = column[j]
    return state
################################# ADD ROUND KEY ################################################
def add_round_key(state, round_key, print_round_key=False):
    round_key = transpose(round_key)
    if print_round_key:
        print("        Round key")
        visualize(round_key)
    for i in range(16):
        state[i] ^= round_key[i]
    return state


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