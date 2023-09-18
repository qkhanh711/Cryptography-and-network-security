from config import *
from utils import *

def encrypt(pt, rkb, rk):
	pt = hex2bin(pt)

	pt = permute(pt, initial_perm, 64)
	print("After initial permutation", bin2hex(pt))

	# Splitting
	left = pt[0:32]
	right = pt[32:64]
	for i in range(0, 16):
		right_expanded = permute(right, exp_d, 48)

		xor_x = xor(right_expanded, rkb[i])

		sbox_str = ""
		for j in range(0, 8):
			row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
			col = bin2dec(
				int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
			val = sbox[j][row][col]
			sbox_str = sbox_str + dec2bin(val)

		sbox_str = permute(sbox_str, per, 32)

		result = xor(left, sbox_str)
		left = result

		if(i != 15):
			left, right = right, left
		print("Round ", i + 1, " ", bin2hex(left),
			" ", bin2hex(right), " ", rk[i])

	combine = left + right

	cipher_text = permute(combine, final_perm, 64)
	return cipher_text

if __name__ == "__main__":
	import argparse as args
	parser = args.ArgumentParser()
	parser.add_argument("-p", "--plaintext", default= "02468ACEECA86420", help="Plain Text")	
	parser.add_argument("-k", "--key", default="0F1571C947D9E859", help="Key")
	args = parser.parse_args()
	pt = args.plaintext
	key = args.key

	print("Plain Text: ", pt)
	print("Key       : ", key)

	rkb, rk = Key_chedule(key)
	print("Encryption")
	cipher_text = bin2hex(encrypt(pt, rkb, rk))
	print("Cipher Text : ", cipher_text)

	print("Decryption")
	rkb_rev = rkb[::-1]
	rk_rev = rk[::-1]
	text = bin2hex(encrypt(cipher_text, rkb_rev, rk_rev))
	print("Plain Text : ", text)
#%%
