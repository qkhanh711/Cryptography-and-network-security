from config import *

def hex2bin(hex):
    return bin(int(hex, 16))[2:].zfill(len(hex) * 4)

def bin2hex(bin):
    return hex(int(bin, 2))[2:].zfill(len(bin) // 4).upper()

def bin2dec(binary):

	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal


def dec2bin(num):
	res = bin(num).replace("0b", "")
	if(len(res) % 4 != 0):
		div = len(res) / 4
		div = int(div)
		counter = (4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res


def permute(k, arr, n):
	permutation = ""
	for i in range(0, n):
		permutation = permutation + k[arr[i]]
	return permutation


def shift_left(k, nth_shifts):
	s = ""
	for i in range(nth_shifts):
		for j in range(1, len(k)):
			s = s + k[j]
		s = s + k[0]
		k = s
		s = ""
	return k

def xor(a, b):
	ans = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			ans = ans + "0"
		else:
			ans = ans + "1"
	return ans

def Key_chedule(key):
	key = hex2bin(key)
	key = permute(key, keyp, 56)

	shift_table = [1, 1, 2, 2,
				   2, 2, 2, 2,
				   1, 2, 2, 2,
				   2, 2, 2, 1]
	left = key[0:28]
	right = key[28:56]
	rkb = []
	rk = []
	for i in range(0, 16):
		left = shift_left(left, shift_table[i])
		right = shift_left(right, shift_table[i])

		combine_str = left + right

		round_key = permute(combine_str, key_comp, 48)

		rkb.append(round_key)
		rk.append(bin2hex(round_key))
	print(len(rkb), len(rk))
	return rkb, rk