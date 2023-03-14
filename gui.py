import tkinter as tk
import customtkinter
from bitarray import bitarray
from bitarray.util import ba2int
from processor import Processor
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")


class Window():
    def __init__(self):
        self.processor=Processor("C:\\Users\Lenovo\Desktop\CS204-Project\CS204-Project\data.mc")
        self.window = customtkinter.CTk()
        self.window.title("RISC-V Simulator")

    def CreateButtons(self):
        frame0 = tk.Frame(master=self.window, width=1000, height=50)
        frame0.pack(fill=tk.Y, side=tk.TOP)
        self.buttonframe = frame0
        step = tk.Button(frame0, text="Step", font=30, border=4,command=self.step)
        step.grid(row=0, column=1)
        run = tk.Button(frame0, text="Run", font=30, border=4)
        run.grid(row=0, column=2)
        run = tk.Button(frame0, text="Dump", font=30, border=4)
        run.grid(row=0, column=3)
        run = tk.Button(frame0, text="Reset", font=30, border=4)
        run.grid(row=0, column=4)

    def pushinstructions(self):
        Ins=self.processor.return_inst()
        self.Insframe = tk.Frame(master=self.window, width=500, height=700)
        self.Insframe.pack(fill=tk.Y, side=tk.LEFT)
        self.Ins=Ins
        # Create a canvas widget
        canvas = tk.Canvas(self.Insframe, width=500, height=700)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar widget
        scrollbar = tk.Scrollbar(self.Insframe, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Set the canvas to adjust its size based on the size of its contents
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Create a frame inside the canvas to hold the instruction set labels
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')
        label = tk.Label(text="Instruction Set", master=frame, font=30, border=1)
        label.grid(row=0)
        label = tk.Label(text=" ", master=frame, font=30, border=1)
        label.grid(row=1)
        rn = 2
        self.instlabels=[]
        index = 0

        for i in Ins:


            label = tk.Label(text=i.split()[0], master=frame, font=30, border=10)
            label.grid(row=rn, column=0)

            if index==0:
                label = tk.Label(text=i.split()[1], master=frame, font=30, border=10, bg = "lightblue")
                label.grid(row=rn, column=1)
            else:
                label = tk.Label(text=i.split()[1], master=frame, font=30, border=10)
                label.grid(row=rn, column=1)

            self.instlabels.append(label)

            rn+=1
            index+=1




        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

    def Display(self):
        self.window.mainloop()

    def Memory(self):

        self.memframe=frame2 = tk.Frame(master=self.window, width=500, height=700, padx=10, pady=10)
        frame2.pack(fill=tk.Y, side=tk.LEFT)

        self.memlabels=[]
        label = tk.Label(text="Memory locations", master=frame2, font=30, border=1)
        label.grid(row=0)
        label = tk.Label(text=" ", master=frame2, font=30, border=1)
        label.grid(row=1)
        adr = 0
        for i in range(20):

            tempLabel = []
            l1,l2,l3,l4=self.processor.memory.mem[adr:adr+8],self.processor.memory.mem[adr+8:adr+16],self.processor.memory.mem[adr+16:adr+24],self.processor.memory.mem[adr+24:adr+32]
            l1 = ba2int(l1)
            l2 = ba2int(l2)
            l3 = ba2int(l3)
            l4 = ba2int(l4)
            l1 = hex(l1)
            l2 = hex(l2)
            l3 = hex(l3)
            l4 = hex(l4)

            label = tk.Label(text=hex(adr), master=self.memframe, font=30, border=1)
            label.grid(row=i+3,column=0)
            tempLabel.append(label)
            label = tk.Label(text=l1, master=self.memframe, font=30, border=1)
            label.grid(row=i+3,column=1)
            tempLabel.append(label)
            label = tk.Label(text=l2, master=self.memframe, font=30, border=1)
            label.grid(row=i+3,column=2)
            tempLabel.append(label)
            label = tk.Label(text=l3, master=self.memframe, font=30, border=1)
            label.grid(row=i+3,column=3)
            tempLabel.append(label)
            label = tk.Label(text=l4 , master=self.memframe, font=30, border=1)
            label.grid(row=i+3,column=4)
            tempLabel.append(label)
            label = tk.Label(text="                  " , master=self.memframe, font=30, border=1)
            label.grid(row=i+3,column=5)
            tempLabel.append(label)
            self.memlabels.append(tempLabel)
            adr+=32

        label = tk.Label(text="" , master=self.memframe, font=30, border=1)
        label.grid(row=24)
        label = tk.Label(text="" , master=self.memframe, font=30, border=1)
        label.grid(row=25)
        label = tk.Label(text="" , master=self.memframe, font=30, border=1)
        label.grid(row=26)
        label= tk.Label(text="Address Value", master=frame2,font=30,border=1)
        label.grid(row=27,column=0)
        entry=tk.Entry(frame2,font=30,border=1)
        entry.grid(row=28)
        def getaddr():
            address=entry.get()
            self.memshow(address)
            entry.delete(0,tk.END)

            return address

        button= tk.Button(frame2,text="Load",font=30,border=1,command=getaddr)
        button.grid(row=28,column=2)

    def RF(self):

            canvas = tk.Canvas(master=self.window, height=700, width=500)
            scroll_y = tk.Scrollbar(master=self.window, orient=tk.VERTICAL, command=canvas.yview)
            scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
            scroll_y.config(command=canvas.yview)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            canvas.configure(yscrollcommand=scroll_y.set)
            canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

            # Add the Register File frame to the scrollable frame
            self.registerframe=registerframe = tk.Frame(master=canvas,)
            canvas.create_window((0, 0), window=registerframe, anchor='nw')
            self.reglabels=[]
            label = tk.Label(text="Register File", master=registerframe, font=30, border=1)
            label.grid(row=0, column=0)
            label = tk.Label(text=" ", master=registerframe, font=30, border=1)
            label.grid(row=1)
            for i in range(32):
                label = tk.Label(text="x"+str(i)+"          ", master=registerframe, font=30, border=1)
                label.grid(row=i+2, column=0)
            for i in range(32):
                label = tk.Label(text="values"+str(i)+"          ", master=registerframe, font=30, border=1)
                label.grid(row=i+2, column=1)
                self.reglabels.append(label)
    def RFupdate(self, RF):
        i=0
        for label in self.reglabels:
            label.config(text=str(self.processor.RF.rf[i]))
            i+=1



    def memshow(self,addr):
        adr = int(addr, 16)
        for label in self.memlabels :
            l1,l2,l3,l4=self.processor.memory.mem[adr:adr+8],self.processor.memory.mem[adr+8:adr+16],self.processor.memory.mem[adr+16:adr+24],self.processor.memory.mem[adr+24:adr+32]
            l1 = ba2int(l1)
            l2 = ba2int(l2)
            l3 = ba2int(l3)
            l4 = ba2int(l4)
            l1 = hex(l1)
            l2 = hex(l2)
            l3 = hex(l3)
            l4 = hex(l4)

            # print(label)

            label[0].config(text=hex(adr))
            label[1].config(text=l1)
            label[2].config(text=l2)
            label[3].config(text=l3)
            label[4].config(text=l4)
            adr+=32

    def instupdate(self):
        pass

    def step(self):
        x = self.processor.PC//32
        self.processor.step()
        self.RFupdate(self.processor.RF.readfile())
        # self.instupdate((self.processor.PC)/32)
        # self.memupdate(self.processor.memory)
        self.instlabels[x].config(bg="white")
        self.instlabels[(self.processor.PC)//32].config(bg="lightblue")

    def run(self):
        self.processor.run()
        self.RFupdate(self.processor.RF.readfile())
