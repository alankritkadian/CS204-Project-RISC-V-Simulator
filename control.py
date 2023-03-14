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
    
