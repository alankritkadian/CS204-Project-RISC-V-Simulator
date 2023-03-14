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


    def decode(self):
        self.currInst.opcode=self.currInst.Inst&127
        self.currInst.rd=(self.currInst.Inst>>7)&31
        self.currInst.funct3=(self.currInst.Inst>>12)&7
        self.currInst.rs1=(self.currInst.Inst>>15)&31
        self.currInst.rs2=(self.currInst.Inst>>20)&31
        self.currInst.funct7=(self.currInst.Inst>>25)&127

        temp = int2ba(self.currInst.Inst,length=32,signed=False)

        imm = temp[0:12]
        self.currInst.imm=ba2int(imm,signed=True)

        immS = temp[0:7]
        immS += temp[20:25]
        self.currInst.immS=ba2int(immS,signed=True)

        immB = bitarray(0)
        immB.append(temp[0])
        immB.append(temp[24])
        immB += temp[1:7]
        immB += temp[20:24]
        immB.append(0)
        # print("Instruction:-",temp)
        #print("immB:-",immB)
        self.currInst.immB = ba2int(immB,signed=True)

        immU=temp[0:20]
        immU+=zeros(12)
        self.currInst.immU=ba2int(immU,signed=True)

        immJ=bitarray(0)
        immJ.append(temp[0])
        immJ+=temp[12:20]
        immJ.append(temp[11])
        immJ+=temp[1:11]
        immJ.append(0)
        self.currInst.immJ+= ba2int(immJ,signed=True)

        self.currInst.op1=self.RF.read(self.currInst.rs1)
        self.currInst.op2=self.RF.read(self.currInst.rs2)
        self.control.Type_gen()
        #print("Instruction Opcode:- ",self.currInst.opcode)
