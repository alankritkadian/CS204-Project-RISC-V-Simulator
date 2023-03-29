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
            # print(int(instructions[i],16))
            self.memory.write_word(32*i,int2ba(int(instructions[i],16),length = 32,signed=False))

    def return_inst(self):
        # print(self.inst_array)
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
        print("imm:-",self.currInst.imm)

        immS = temp[0:7]
        immS += temp[20:25]
        self.currInst.immS=ba2int(immS,signed=True)
        print("immS:-",self.currInst.immS)

        immB = bitarray(0)
        immB.append(temp[0])
        immB.append(temp[24])
        immB += temp[1:7]
        immB += temp[20:24]
        immB.append(0)
        self.currInst.immB = ba2int(immB,signed=True)
        print("immB:-",self.currInst.immB)

        immU=temp[0:20]
        immU+=zeros(12)
        self.currInst.immU=ba2int(immU,signed=True)
        print("immU:-",self.currInst.immU)

        immJ=bitarray(0)
        immJ.append(temp[0])
        immJ+=temp[12:20]
        immJ.append(temp[11])
        immJ+=temp[1:11]
        immJ.append(0)
        self.currInst.immJ = ba2int(immJ,signed=True)
        print("immJ:-",self.currInst.immJ)

        self.currInst.op1=self.RF.read(self.currInst.rs1)
        self.currInst.op2=self.RF.read(self.currInst.rs2)
        self.control.Type_gen()
        print("Instruction Opcode:- ",self.currInst.opcode)

    def sign_extend(self):
        if self.currInst.imm>>11==1:
            self.currInst.imm = self.currInst.imm - 2 ** 12
        if self.currInst.immB>>12==1:
            self.currInst.immB=self.currInst.immB - 2 ** 13
        if self.currInst.immS>>11==1:
            self.currInst.immS=self.currInst.immS - 2 ** 12
        if self.currInst.immU>>31==1:
            self.currInst.immU=self.currInst.immU - 2 ** 32
        if self.currInst.immJ>>20==1:
            self.currInst.immJ=self.currInst.immJ - 2 ** 21

    def execute(self):
        self.control.OP2Select_gen()
        self.control.ALUOp_gen()
        self.ALU = ALU(self.currInst,self.control)
        self.ALUResult=self.ALU.execute()
        self.control.BranchTargetSelect_gen()
        print("Intruction Type:- ",self.control.type,"ALUResult:- ",self.ALUResult)

    def memory_access(self):
        if self.control.ALUOp=="sb":
            s = int2ba(self.currInst.op2,length=32,signed=True)
            self.memory.write_byte(self.ALUResult,s[24:32])
            print("Memory Access:- ","sb")
            print("writeback at ",self.ALUResult,"with data ",s[24:32])
        elif self.control.ALUOp=="sh":
            s = int2ba(self.currInst.op2,length=32,signed=True)
            self.memory.write_halfword(self.ALUResult,s[16:32])
            print("Memory Access:- ","sh")
            print("writeback at ",self.ALUResult,"with data ",s[16:32])
        elif self.control.ALUOp=="sw":
            s = int2ba(self.currInst.op2,length=32,signed=True)
            self.memory.write_word(self.ALUResult,s)
            print("Memory Access:- ","sw")
            print("writeback at ",self.ALUResult,"with data ",s)
        elif self.control.ALUOp=="lb":
            self.currInst.LoadData=ba2int(self.memory.load_byte(self.ALUResult),signed=True)
            print("Memory Access:- ","lb")
            print("load word from ",self.ALUResult,"with data ",self.currInst.LoadData)
        elif self.control.ALUOp=="lh":
            self.currInst.LoadData=ba2int(self.memory.load_halfword(self.ALUResult),signed=True)
            print("Memory Access:- ","lh")
            print("load word from ",self.ALUResult,"with data ",self.currInst.LoadData)
        elif self.control.ALUOp=="lw":
            self.currInst.LoadData=ba2int(self.memory.load_word(self.ALUResult),signed=True)
            print("Memory Access:- ","lw")
            print("load word from ",self.ALUResult,"with data ",self.currInst.LoadData)

    def write_back(self):
        self.control.ResultSelect_gen()
        temp=self.control.ResultSelect
        #Write Back in Rd
        if temp==0:
            self.RF.write(self.currInst.rd,self.ALUResult)
        elif temp==1:
            self.RF.write(self.currInst.rd,self.currInst.LoadData)
        elif temp==2:
            self.RF.write(self.currInst.rd,self.PC+32)
        elif temp==3:
            self.RF.write(self.currInst.rd,self.currInst.immU)
        elif temp==4:
            self.RF.write(self.currInst.rd,self.currInst.immU*8+self.PC)

        #Updating Branch Target Address
        if self.control.BranchTargetSelect==0:
            self.currInst.BranchTargetAddress=self.currInst.immB*8+self.PC
        else:
            self.currInst.BranchTargetAddress=self.currInst.immJ*8+self.PC

        self.control.isBranch_gen(self.ALUResult)
        print("isBranch:-",self.control.isBranch) 
        #Update PC
        if self.control.isBranch==0:
            self.PC+=32            
        elif self.control.isBranch==1:
            self.PC=self.currInst.BranchTargetAddress
        else:
            self.PC=self.ALUResult

        print("PC:-",self.PC)

    def memory_return(self):
        return self.memory.mem

    def return_RF(self):
        return self.RF.readfile()
    
    def run(self):
        self.PC=0
        self.clock=0
        while 1:
            if self.step()==0:
                break
            self.clock+=1
        
        print("Clock:-",self.clock)
        # print(self.RF.readfile())
        
    def step(self):
        x = self.fetch()
        if x==0: 
            return 0
        self.decode()
        self.execute()
        self.memory_access()
        self.write_back()
        return 1
