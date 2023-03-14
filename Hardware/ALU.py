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

    def execute(self):
        self.ALUoperands()
        operation = self.Control.ALUOp
        if operation == "add" or operation=="addi":
            return self.operand1+self.operand2
        elif operation == "sub":
            return self.operand1-self.operand2
        elif operation == "xor":
            return self.operand1^self.operand2
        elif operation == "or" or operation=="ori":
            return self.operand1|self.operand2
        elif operation == "and" or operation=="andi":
            return self.operand1&self.operand2
        elif operation == "srl":
            x = int2ba(self.operand1,length=32,signed=True)
            y = zeros(self.operand2)
            x = y+x
            x = x[0:32]
            x = ba2int(x)
            return x
        elif operation == "sll":
            return self.operand1<<self.operand2
        elif operation == "sra":
            return self.operand1>>self.operand2
        elif operation == "slt": 
            if self.operand1<self.operand2:  
                return 1
            else:
                return 0
        elif operation=="lb" or operation=="lw" or operation=="lh" :
            return self.operand1+self.operand2
        elif operation=="sb" or operation=="sw" or operation=="sh":
            return self.operand1+self.operand2
        elif operation == "beq":
            if self.operand1==self.operand2:
                return 1                
            else:
                return 0
        elif operation == "bne":
            if self.operand1!=self.operand2:
                return 1
            else:
                return 0
        elif operation == "blt":
            if self.operand1<self.operand2:
                return 1
            else:
                return 0
        elif operation == "bge":
            if self.operand1>=self.operand2:
                return 1
            else:
                return 0
        elif operation == "jalr":
            return self.operand1+self.operand2
        elif operation == "jal":      
            return "jal"
        elif operation=="lui" or operation=="auipc":
            return "Utype"
        elif operation == "error":
            print("error")
            return 0