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