from config import sbox, sboxInv, rcon

################################# KEY SCHEDULE ################################################
def keyScheduleCore(word, i):
    word = rotate(word, 1)
    newWord = []
    for byte in word:
        newWord.append(sbox[byte])
    newWord[0] = newWord[0] ^ rcon[i]
    return newWord

def expandKey(cipherKey, key_length):
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
def substitute_bytes(state):
    result_hex = []
    for byte_hex in state:
        # byte_int = int(byte_hex, 16)
        substituted_byte = sbox[byte_hex]
        result_hex.append(format(substituted_byte, '02x'))  
    return result_hex

################################# SHIFT ROWS ################################################
def rotate(word, n):
    return word[n:]+word[0:n]

def shift_rows(state):
    for i in range(4):
        state[i*4:i*4+4] = rotate(state[i*4:i*4+4],i)
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

def mixColumn(column):
    temp = column.copy()
    column[0] = galoisMult(temp[0], 2) ^ galoisMult(temp[3], 1) \
                ^ galoisMult(temp[2], 1) ^ galoisMult(temp[1], 3)
    column[1] = galoisMult(temp[1], 2) ^ galoisMult(temp[0], 1) \
                ^ galoisMult(temp[3], 1) ^ galoisMult(temp[2], 3)
    column[2] = galoisMult(temp[2], 2) ^ galoisMult(temp[1], 1) \
                ^ galoisMult(temp[0], 1) ^ galoisMult(temp[3], 3)
    column[3] = galoisMult(temp[3], 2) ^ galoisMult(temp[2], 1) \
                ^ galoisMult(temp[1], 1) ^ galoisMult(temp[0], 3)

def mixColumns(state):
    for i in range(4):
        column = []
        for j in range(4):
            column.append(state[j * 4 + i])
        mixColumn(column)
        # Transfer the new values back into the state table
        for j in range(4):
            state[j * 4 + i] = column[j]
    return state

################################# ADD ROUND KEY ################################################
def add_round_key(state, round_key):
    for i in range(16):
        state[i] ^= round_key[i]
    return state


################################# ENCRYPTOR ################################################

def text_to_states(plaintext, option = 'char', key = False):

    if key:
        for i in range(0, len(plaintext), len(plaintext)):
            if option == 'char':
                hex_state = [hex(ord(char))[2:].zfill(2) for char in plaintext]
                # print(hex_state)
            else:
                hex_state = [int(char.encode('utf-8').hex(), 16) for char in plaintext]
        return hex_state
    else:
        while len(plaintext) % 16 != 0:
            plaintext += ' '  

        states = []
        for i in range(0, len(plaintext), 16):
            state = plaintext[i:i+16]
            if option == 'char':
                hex_state = [hex(ord(char))[2:].zfill(2) for char in state]
                # print(hex_state)
            else:
                hex_state = [int(char.encode('utf-8').hex(), 16) for char in state]
            states.append(hex_state)

        return states

def cvrt_hex(plaintext, option = 'int'):
    for i in range(0, len(plaintext)):
        state = plaintext
        if option == 'char':
            hex_state = [hex(ord(char))[2:].zfill(2) for char in state]
            print(hex_state)
        else:
            hex_state = [int(char.encode('utf-8').hex(), 16) for char in state]

    return hex_state

################################# DECRYPTOR ################################################

def states_to_text(hex_states):
    plaintext = "".join([chr(hex_char) for hex_char in hex_states])
    return plaintext

def encryptBlock(state, roundKeys):
    roundKeyIndex = 0

    add_round_key(state, roundKeys[:16])

    for round in range(1, 10):
        substitute_bytes(state)
        shift_rows(state)
        mixColumns(state)
        add_round_key(state, roundKeys[roundKeyIndex + 16:roundKeyIndex + 32])
        roundKeyIndex += 16

    substitute_bytes(state)
    shift_rows(state)
    add_round_key(state, roundKeys[160:])

    # Chuyển đổi trạng thái trở lại dạng hex
    state = [format(byte, '02x') for byte in state]
    
    return state

def encrypt(plaintext, cipherKey, key_length=176):
    expandedKey = expandKey(cipherKey, key_length)
    visualize = text_to_states(plaintext)
    states = text_to_states(plaintext, option="int")
    cipherKey = text_to_states(cipherKey, option="int")
    print(states)
    print (cipherKey)
    ciphertext = []

    for state in states:
        state = encryptBlock(state, expandedKey)
        ciphertext.extend(state)

    return "".join(ciphertext)

# plaintext = "0123456789abcdeffedcba9876543210"
# key = "0f1571c947d9e8590cb7add6af7f6798"

# ciphertext = encrypt(plaintext, key, key_length=16)
# print("Mã hóa:", ciphertext)
