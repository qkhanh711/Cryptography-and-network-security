import random

class Diffie_Hellman():
    def __init__(self, p, alpha, Xa, Xb, option = "random"):
        self.p = p
        self.alpha = alpha
        if option == "random":
            self.Xa = random.randint(1, p)
            self.Xb = random.randint(1, p)
        else:
            self.Xa = Xa
            self.Xb = Xb
        self.Ya = self.alpha ** self.Xa % self.p # Alpha mu Xa mod p
        self.Yb = self.alpha ** self.Xb % self.p
        self.Ka = self.Yb ** self.Xa % self.p
        self.Kb = self.Ya ** self.Xb % self.p

    def is_prime(self, n):
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5)+1, 2):
            if n % i == 0:
                return False
        return True
        
    def checkGenerator(self, alpha, p):
        if alpha > 1:
            for i in range(1, p):
                if (alpha ** i) % p == 1:
                    if pow(alpha, (p-1)/i) == 1:
                        return False
            return True
        else:
            return False

    def main(self):
        if self.Xa > self.p or self.Xb > self.p:
            print("Xa or Xb is bigger than p \n Choose value less than p")
            return
        # print("q: ", self.q)
        if self.is_prime(self.p) == False:
            print("p is not a prime number")
            return
        print("alpha: ", self.alpha)
        if self.checkGenerator(self.alpha, self.p) == False:
            print("alpha is not a primitive root of Zq*")
            return
        print("Xa: ", self.Xa)
        print("Xb: ", self.Xb)
        print("Ya: ", self.Ya)
        print("Yb: ", self.Yb)
        print("Ka: ", self.Ka)
        print("Kb: ", self.Kb)
    
