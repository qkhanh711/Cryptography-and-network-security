import random
import math 

class RSAEncryptDecrypt:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        while self.p == self.q:
            self.q = self.generate_prime()
        
        self.n = self.p * self.q
        self.phi_n = (self.p-1) * (self.q-1)
        self.e = self.generate_public_key()
        self.d = self.mod_inverse()

    def is_prime(self, n):
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5)+1, 2):
            if n % i == 0:
                return False
        return True

    def generate_prime(self):
        while True:
            p = random.randint(self.min_value, self.max_value)
            if self.is_prime(p): 
                return p

    def generate_public_key(self):
        e = random.randint(2, self.phi_n)
        while math.gcd(e, self.phi_n) != 1:
            e = random.randint(2, self.phi_n)
        return e

    def mod_inverse(self):
        for i in range(2, self.phi_n):
            if (self.e * i) % self.phi_n == 1:
                return i
        raise Exception("No mod inverse found")

    def encrypt(self, plaintext):
        plaintext_encode = [ord(char) for char in plaintext]
        ciphertext = [pow(char, self.e, self.n) for char in plaintext_encode]
        return ciphertext

    def decrypt(self, ciphertext):
        decrypted = [pow(char, self.d, self.n) for char in ciphertext]
        message = "".join([chr(char) for char in decrypted])
        return message

    def get_public_key(self):
        return {"e": self.e
                ,"n": self.n}

    def get_private_key(self):
        return {"d": self.d,
                "n": self.n}


if __name__ == "__main__":
    min_value = 100
    max_value = 1000
    rsa = RSAEncryptDecrypt(min_value, max_value)

    plaintext = "Hello World"
    print(f"plaintext: {plaintext}")

    ciphertext = rsa.encrypt(plaintext)
    print(f"ciphertext: {ciphertext}")

    decrypted_message = rsa.decrypt(ciphertext)
    print(f"decrypted message: {decrypted_message}")

    public_key = rsa.get_public_key()
    private_key = rsa.get_private_key()
    print(f"Public key: {public_key}")
    print(f"Private key: {private_key}")

    print(f"p value {rsa.p} and q value {rsa.q}")
