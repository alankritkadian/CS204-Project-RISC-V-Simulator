from Hardware.register import RF
# from Hardware.mux import *
from Hardware.memory import Memory
from Hardware.ALU import ALU
from control import Control
from bitarray import bitarray
from bitarray.util import ba2int, int2ba,zeros
# from Hardware.register import *


class Environment:
    def __init__(self):  
        self.opcode=0      
        self.Inst=0
        self.rd=0
        self.rs1=0
        self.rs2=0
        self.immB=0
        self.imm=0
        self.immS=0
        self.immU=0
        self.immJ=0
        self.op1=0
        self.op2=0
        self.funct3=0
        self.funct7=0
        self.LoadData=0
        self.BranchTargetAddress=0

class Processor:
    def __init__(self,filePath):
        self.PC=0
        self.RF=RF()
        self.memory=Memory()
        self.currInst=Environment()
        self.control=Control(self.currInst)
        self.inst_array=[]
        self.load_from_file(filePath)

    def load_from_file(self,filePath):
        file=open(filePath,"r")
        instructions=[]
        for temp in file:
            self.inst_array.append(temp)
            instructions.append(temp.split()[1])
        file.close()
        for i in range(0,len(instructions)):
            print(int(instructions[i],16))
            self.memory.write_word(32*i,int2ba(int(instructions[i],16),length = 32,signed=False))
    
    def return_inst(self):
        print(self.inst_array)
        return self.inst_array

    def fetch(self):
        self.currInst.Inst=ba2int(self.memory.load_word(self.PC),signed=False) # currinst stores current instruction
        print("Instruction Fetched:- ",self.currInst.Inst)
        return self.currInst.Inst