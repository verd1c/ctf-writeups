# JavaScript VM

## tl;dr 

A binary built using a Virtual Machine built on NodeJS

## Analysis

We get given an [open source JavaScript VM](https://github.com/francisrstokes/16bitjs) and a binary file compiled using it's compiler.

 By running the binary in the VM we can see that it asks for the flag 1 character at a time. 52 characters are required for the flag:

![Start](img/init_start.png)

and ends with "Wrong":

![Start](img/init_end.png)



## Disassembling

In order to see some sort of source code and try and analyze, I studied the VM's behavior with different instructions to be able to reconstruct the pseudo-assembly given the binary file.

To begin with, the VM runs on 16-bit (2-byte) instructions. Using the VM's


I've included my python disassembler both as a file and at the end of this README.

## Discovering Calls

We can see the following reoccuring pattern
```asm
0x2: MVI D 75
0x3: AUI D 0
0x4: CAL D (0x4b)
```

```
0xe: MVI D 156
0xf: AUI D 0
0x10: CAL D (0x9c);
```

```
0x11: MVI D 211
0x12: AUI D 0
0x13: CAL D (0xd3);
```

This means that we can distinguish 3 different functions that are being called from the program's start that we will see below.



## Input

## Swirl

## Mapper

## Decryptor

We import the 3 52-byte arrays that we found above into a python script - the swirl array (256 + 32), the mapper array (256 + 132) and the encrypted flag (256 + 191).

The original obfuscation is given by the following algorithm:
```
input_flag <- input()

loop from 0 to 31:
    swirl(input_flag)
    wrap(input_flag)
    
if in == encrypted_flag:
    correct
```

This encryption can be reversed as:

```
input <- encrypted_flag

loop from 31 to 0:
    swirl_backwards(input)
    wrap_backwards(input)

print("Flag: " + input)
```

With swirl_backwards and wrap_backwards just doing the same as swirl and wrap but in reverse order (from 51 to 0)

```python
# 32
swirl = [28,10,17,38,37,13,26,14,25,23,3,15,21,18,41,19,4,16,5,39,8,32,27,33,11,0,34,46,36,35,51,47,22,6,40,2,29,7,24,45,12,44,31,30,49,43,48,42,50,1,20,9]

# 132
mapper = [0x61,0x65,0x71,0x75,0x65,0x6f,0x73,0x61,0x6c,0x69,0x6e,0x6f,0x63,0x61,0x6c,0x63,0x61,0x6c,0x69,0x6e,0x6f,0x63,0x65,0x72,0x61,0x63,0x65,0x6f,0x61,0x6c,0x75,0x6d,0x69,0x6e,0x6f,0x73,0x6f,0x63,0x75,0x70,0x72,0x65,0x6f,0x76,0x69,0x74,0x72,0x69,0x6f,0x6c,0x69,0x63]

# 191
encoded_flag = [0x7f,0x94,0xd4,0xf2,0xf7,0xaf,0x98,0xba,0x9e,0xd7,0x85,0xb3,0xfb,0xdd,0xcf,0xb7,0xe6,0x5e,0x03,0xaf,0xd8,0xb3,0xc3,0xb7,0xbe,0xa2,0xbd,0x51,0xaa,0x98,0xd1,0xa4,0xc4,0xa0,0x62,0x61,0x57,0x91,0x58,0x9d,0xf8,0xc5,0xaf,0x88,0xb4,0xba,0xe9,0xaf,0xdf,0xa9,0xb9,0xd9]

flag_len = len(encoded_flag)
def do_swirl():
    for i in reversed(range(flag_len)):
        temp = encoded_flag[i]
        encoded_flag[i] = encoded_flag[swirl[i]]
        encoded_flag[swirl[i]] = temp

def do_ath(swirl_counter):
    for i in reversed(range(flag_len)):
        encoded_flag[i] = (encoded_flag[i] - mapper[(i + swirl_counter + 11) % flag_len]) & 0xFF

for i in reversed(range(32)):
    do_ath(i)
    do_swirl()

print(''.join([chr(c) for c in encoded_flag]))
```

## Flag

## Disassembler

```py
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

constants = {
    'INSTRUCTIONS': [
        'MVR',
        'MVV',
        'LDR',
        'STA',
        'ATH',
        'CAL',
        'JCP',
        'PSH',
        'POP',
        'JMP',
        'JMR',
        'LDA',
        'STR',
        'NOA'
    ],
    'REGISTERS': [
        'A',
        'B',
        'C',
        'D'
    ],
    'ARITHMETIC': [
        'ADD',
        'SUB',
        'MUL',
        'DIV',
        'INC',
        'DEC',

        'LSF',
        'RSF',
        'AND',
        'OR',
        'XOR',
        'NOT'
    ],
    'MOVE': [
        'MVI',
        'ADI',
        'MUI',
        'AUI'
    ],
    'SYSOPS': [
        'NOP',
        'RET',
        'SYS',
        'HALT'
    ],
    'JUMP': [
        'EQ',
        'NEQ',
        'LT',
        'GT',
        'LTE',
        'GTE',
        'ZER',
        'NZE'
    ]
}

registers = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0
}

sBinary = open('chall.bin', 'rb').read()
print(len(sBinary))

lFuncCounter = 1
lLastFuncOffset = 0
fFunctions = {}

for lIter in range(0, math.floor(len(sBinary)), 2):
    lInstrOffset = math.floor(lIter / 2)
    iBitInstr = bin(sBinary[lIter+1])[2:].zfill(8) + bin(sBinary[lIter])[2:].zfill(8)

    iOpCode = int(iBitInstr[12:16], 2)
    sOpCode = constants['INSTRUCTIONS'][iOpCode]

    # Registers
    rDest = int(iBitInstr[10:12], 2)

    if sOpCode == 'ATH':
        iOperation = int(iBitInstr[4:8], 2)
        bShiftVal = int(iBitInstr[:3], 2)
        rSrc = int(iBitInstr[8:10], 2)
        mMode = int(iBitInstr[3], 2)

        if mMode == 1:
            sOutInstr = f"{hex(lInstrOffset)}: {constants['ARITHMETIC'][iOperation]} {constants['REGISTERS'][rSrc]} {constants['REGISTERS'][rDest]}"
        else:
            sOutInstr = f"{hex(lInstrOffset)}: {constants['ARITHMETIC'][iOperation]} {constants['REGISTERS'][rDest]} {constants['REGISTERS'][rSrc]}"
        
    elif sOpCode == 'CAL':

        fFunctions[lLastFuncOffset] = f"unnamed_{lFuncCounter}"
        lFuncCounter += 1
        sOutInstr = f"{hex(lInstrOffset)}: {bcolors.OKCYAN}{constants['INSTRUCTIONS'][iOpCode]} {constants['REGISTERS'][rDest]} {bcolors.ENDC}{bcolors.OKGREEN}({hex(lLastFuncOffset)}){bcolors.ENDC}"
    elif sOpCode == 'MVV':
        iOperation = int(iBitInstr[8:10], 2)
        sOperation = constants['MOVE'][iOperation]
        rValue = int(iBitInstr[:8], 2)

        if sOperation == 'MVI':
            lLastFuncOffset = rValue

        sOutInstr = f"{hex(lInstrOffset)}: {sOperation} {constants['REGISTERS'][rDest]} {rValue}"
    elif sOpCode == 'JMR':
        rSrc = int(iBitInstr[8:10], 2)

        sOutInstr = f"{hex(lInstrOffset)}: {constants['INSTRUCTIONS'][iOpCode]} {constants['REGISTERS'][rSrc]}"
    elif sOpCode == 'NOA':
        iOperation = int(iBitInstr[8:12], 2)
        sOperation = constants['SYSOPS'][iOperation]

        sOutInstr = f"{hex(lInstrOffset)}: {bcolors.HEADER}{constants['SYSOPS'][iOperation]}{bcolors.ENDC}"
    elif sOpCode == 'PSH':
        rSrc = int(iBitInstr[8:10], 2)

        sOutInstr = f"{hex(lInstrOffset)}: {constants['INSTRUCTIONS'][iOpCode]} {constants['REGISTERS'][rSrc]}"
    elif sOpCode == 'POP':

        sOutInstr = f"{hex(lInstrOffset)}: {constants['INSTRUCTIONS'][iOpCode]} {constants['REGISTERS'][rDest]}"
    elif sOpCode == 'LDA':
        lAddr = hex(int(iBitInstr[:10], 2))

        sOutInstr = f"{hex(lInstrOffset)}: {constants['INSTRUCTIONS'][iOpCode]} {constants['REGISTERS'][rDest]} {lAddr}"
    elif sOpCode == 'LDR':
        rSrc = int(iBitInstr[8:10], 2)
        lOffset = hex(int(iBitInstr[:8], 2))

        sOutInstr = f"{hex(lInstrOffset)}: {constants['INSTRUCTIONS'][iOpCode]} {constants['REGISTERS'][rDest]} {bcolors.OKGREEN}{lOffset}{bcolors.ENDC}[{rSrc}]"
    elif sOpCode == 'JCP':
        iOperation = int(iBitInstr[3:6], 2)
        rSrc = int(iBitInstr[8:10], 2)
        lAddr = int(iBitInstr[6:8], 2)

        sOutInstr = f"{hex(lInstrOffset)}: {constants['JUMP'][iOperation]} {constants['REGISTERS'][rSrc]} {constants['REGISTERS'][rDest]} {constants['REGISTERS'][lAddr]}"
    elif sOpCode == 'MVR':
        rSrc = int(iBitInstr[8:10], 2)
        vValue = int(iBitInstr[:8], 2)

        sOutInstr = f"{hex(lInstrOffset)}: {constants['INSTRUCTIONS'][iOpCode]} {constants['REGISTERS'][rDest]} {constants['REGISTERS'][rSrc]} {vValue}"
    elif sOpCode == 'STR':
        rSrc = int(iBitInstr[8:10], 2)
        lOffset = hex(int(iBitInstr[:8], 2))

        sOutInstr = f"{hex(lInstrOffset)}: {constants['INSTRUCTIONS'][iOpCode]} {constants['REGISTERS'][rSrc]} {bcolors.OKGREEN}{lOffset}{bcolors.ENDC}[{constants['REGISTERS'][rDest]}]"
    else:
        sOutInstr = f"{hex(lInstrOffset)}: {constants['INSTRUCTIONS'][iOpCode]}"

    if(lInstrOffset in fFunctions):
        print(f"\n{bcolors.WARNING}-- Function {fFunctions[lInstrOffset]} --{bcolors.ENDC}")
    print(sOutInstr)
```