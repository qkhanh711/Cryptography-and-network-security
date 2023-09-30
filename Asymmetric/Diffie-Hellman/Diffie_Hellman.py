import random

class Diffie_Hellman():
    def __init__(self, p, alpha,Xa,Xb, option = "random"):
        self.p = p
        self.alpha = alpha
        if option == "random":
            self.Xa = random.randint(1,p)
            self.Xb = random.randint(1, p)
        else:
            self.Xa = Xa
            self.Xb = Xb
        self.Ya = pow(self.alpha, self.Xa, self.p)
        self.Yb = pow(self.alpha, self.Xb, self.p)
        self.Ka = pow(self.Yb, self.Xa, self.p)
        self.Kb = pow(self.Ya, self.Xb, self.p)
    
    def is_prime(self, n):
        pass