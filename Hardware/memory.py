from bitarray import bitarray
from bitarray.util import ba2int, int2ba, zeros
class Memory():
    def __init__(self, size = pow(2,32)):
        self.size = size
        self.mem = bitarray(size)
        self.mem.setall(0)

    def load_word(self, address):
        word = bitarray(0)
        for i in range(0,4):
            temp = self.load_byte(address + 8*i)
            word += temp
        return word  
    
    def load_halfword(self, address):
        word = bitarray(0)
        for i in range(0,2):
            temp = self.load_byte(address + 8*i)
            word += temp
        return word  

    def load_byte(self, address):
        x = bitarray(0)
        for i in range(0,8):
            x.append(self.mem[address + i])
        return x
    
    def write_word(self, address, data):
        for i in range (0,32):
            self.mem[address+i]=data[i]
    
    def write_halfword(self, address, data):
        for i in range (0,16):
            self.mem[address+i]=data[i]
            
    def write_byte(self,address,data):
        for i in range(0,8):
            self.mem[address+i] = data[i]
        







