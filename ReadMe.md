# RISC-V Simulator
##### _An application to simulate the execution of machine code in RISC-V ISA_
##### _This repository contains a RISC-V Simulator written in Python that can execute RISC-V code._
#

```
Contributors:
Alankrit Kadian      :- 2021CSB1065
Aditya Dinesh Patil  :- 2021CSB1062
Prashant Singh       :- 2021CSB1124
Nakul R. Alawadhi    :- 2021CSB1111
```

### Instructions Supported
```
R format - add, and, or, sll, slt, sra, srl, sub, xor
I format - addi, andi, ori, lb, lh, lw, jalr
S format - sb, sw, sh
SB format - beq, bne, bge, blt
U format - auipc, lui
J format - jal
```


## Run Locally

Clone the project

```bash
  git clone https://github.com/alankritkadian/CS204-Project-RISC-V-Simulator
```

Go to the project directory

```bash
  cd CS204-Project-RISC-V-Simulator/
```

Install dependencies

```bash
  pip install customtkinter
  pip install bitarray
```

Run the project

```bash
  python main.py
```
