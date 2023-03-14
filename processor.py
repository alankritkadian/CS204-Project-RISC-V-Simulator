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