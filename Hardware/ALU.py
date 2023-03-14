from bitarray import bitarray
from bitarray.util import ba2int, int2ba, zeros
class ALU:

    def __init__(self,Environment,Control):
        self.Env = Environment
        self.Control = Control
        self.operand1=self.Env.op1
        self.operand2=self.Env.op2
            
    def ALUoperands(self):
        if self.Control.OP2Select==1:
            self.operand2=self.Env.imm
        elif self.Control.OP2Select==2:
            self.operand2=self.Env.immS

    