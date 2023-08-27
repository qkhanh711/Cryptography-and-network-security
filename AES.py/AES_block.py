from utils import rotate
from copy import copy
class ASE():
    def __init__(self, plaintext, epochs):
        self.plaintext = plaintext
        self.state = plaintext.copy()
        self.epochs = epochs
    
    def add_round_key(self):
        return self.plaintext
    
    def substitute_bytes(self):
        pass
    
    def shift_rows(self):
        for i in range(4):
            self.state[i*4:i*4+4] = rotate(self.state[i*4:i*4+4],i)
    
    def mix_columns(self):
        pass
    
    def Block(self, epoch = None):
        self.substitute_bytes()
        self.shift_rows()
        if epoch != self.epochs:
            self.mix_columns()
        self.add_round_key()
        pass
    
    def Encrypter(self):
        self.add_round_key(self.plaintext)
        for i in range(self.epochs):
            self.Block(epoch=i)
        pass


    
            
