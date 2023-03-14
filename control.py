class Control:
    def __init__(self,Environment):
        self.type=0
        self.isBranch=0
        self.OP2Select=0
        self.RFWrite=0
        self.ALUOp=""
        self.ResultSelect=0
        self.BranchTargetSelect=0
        self.Env = Environment

    def Type_gen(self):
        if self.Env.opcode == 51:
            self.type = "R"
        elif self.Env.opcode == 19 or self.Env.opcode == 3 or self.Env.opcode == 103:
            self.type = "I"
        elif self.Env.opcode == 35:
            self.type = "S"
        elif self.Env.opcode == 55 or self.Env.opcode == 23:
            self.type = "U"
        elif self.Env.opcode == 111:
            self.type = "J"
        elif self.Env.opcode == 99:
            self.type = "B"

    def OP2Select_gen(self):
        if self.type == "R" or self.type == "B":
            self.OP2Select = 0
        elif self.type == "I":
            self.OP2Select = 1
        elif self.type == "S":
            self.OP2Select = 2
    
    def ALUOp_gen(self):
        if self.type == "R":
            if self.Env.funct3 == 0:
                if self.Env.funct7 == 0:
                    self.ALUOp = "add"
                elif self.Env.funct7 == 32:
                    self.ALUOp = "sub"
            elif self.Env.funct3 == 4:
                self.ALUOp = "xor"
            elif self.Env.funct3 == 6:
                self.ALUOp = "or"
            elif self.Env.funct3 == 7:
                self.ALUOp = "and"
            elif self.Env.funct3 == 1:
                self.ALUOp = "sll"
            elif self.Env.funct3 == 5:
                if self.Env.funct7 == 0:
                    self.ALUOp = "srl"
                elif self.Env.funct7 == 32:
                    self.ALUOp = "sra"
            elif self.Env.funct3 == 2:
                self.ALUOp = "slt"
            else:
                self.ALUOp="error"
        elif self.type == "I" and self.Env.opcode == 19:              
            if self.Env.funct3 == 0:
                self.ALUOp = "addi"            
            elif self.Env.funct3 == 6:
                self.ALUOp = "ori"
            elif self.Env.funct3 == 7:
                self.ALUOp = "andi"            
            else:
                self.ALUOp="error"
        elif self.type == "I" and self.Env.opcode == 3:
            if self.Env.funct3 == 0:
                self.ALUOp = "lb"
            elif self.Env.funct3 == 1:
                self.ALUOp = "lh"
            elif self.Env.funct3 == 2:
                self.ALUOp = "lw"            
            else:
                self.ALUOp="error"
        elif self.type == "S" and self.Env.opcode == 35:
            if self.Env.funct3 == 0:
                self.ALUOp = "sb"
            elif self.Env.funct3 == 1:
                self.ALUOp = "sh"
            elif self.Env.funct3 == 2:
                self.ALUOp = "sw"            
            else:
                self.ALUOp="error"
        elif self.type == "I" and self.Env.opcode == 103:
            if self.Env.funct3 == 0:
                self.ALUOp = "jalr"       
            else:
                self.ALUOp="error" 
        elif self.type == "B" :
            if self.Env.funct3 == 0:
                self.ALUOp = "beq"
            elif self.Env.funct3 == 1:
                self.ALUOp = "bne"
            elif self.Env.funct3 == 4:
                self.ALUOp = "blt"            
            elif self.Env.funct3 == 5:
                self.ALUOp = "bge"            
            else:
                self.ALUOp="error"
        elif self.type == "U" :
            if self.Env.opcode == 55:
                self.ALUOp = "lui"
            elif self.Env.opcode == 23:
                self.ALUOp = "auipc"                      
            else:
                self.ALUOp="error"
        elif self.type == "J":
            if self.Env.opcode == 111:
                self.ALUOp = "jal"                      
            else:
                self.ALUOp="error"
    
    def BranchTargetSelect_gen(self):
        if self.type == "J":
            self.BranchTargetSelect = 1 #immJ
        else:
            self.BranchTargetSelect = 0 #immB