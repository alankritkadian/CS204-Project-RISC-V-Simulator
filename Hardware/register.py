class RF():
    def __init__(self) :
        self.rf=[0]*32
        self.rf[2]=2147483612
        self.rf[3]=268435456
        self.rf[10]=1
        self.rf[11]=2147483612

    def write(self,i,val):
        self.rf[i]=val

    def read(self,i):
        return self.rf[i]

    def readfile(self):
        return self.rf
