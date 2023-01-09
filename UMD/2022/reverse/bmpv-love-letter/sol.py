import sys

INSTR = [
    'WIPE',
    'NEGATE',
    'SWAP',
    'DEAL',
    'DEALW',
    'DRAW',
    'DRAWW',
    'JUMP',
    'LOADI',
    'LOADB',
    'STOREB',
    'COPY4',
    'XOR',
    'ADD',
    'BEQ',
    'HALT'
]


binary = open('bmpx/chall.bmpx', 'rb')

# Load into memory
memory = []
byte = binary.read(1)
while byte:
    memory.append(byte)
    byte = binary.read(1)
memptr = 0
binary.close()

def ReadBytes(n):
    global memptr, memory
    bs = b"".join([b for b in memory[memptr:memptr+n]])
    memptr += n
    return bs

def ReadBytesAt(n, at):
    global memory
    bs = b"".join([b for b in memory[at:at+n]])
    return bs

magic = ReadBytes(2)
fsize = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)
fexec = ReadBytes(4)

if magic != b'BM' or fexec != b'EXEC':
    print('Magic bytes dont match with BMPX format.')
    exit()

dataOffest = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)
hsize = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)
width = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)
height = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)
hplanes = int.from_bytes(ReadBytes(2), byteorder=sys.byteorder)
bpx = int.from_bytes(ReadBytes(2), byteorder=sys.byteorder)
hcomp = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)
isize = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)
XpixelsPerM = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)
YpixelsPerM = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)
colorsUsed = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)
colorsImportant = int.from_bytes(ReadBytes(4), byteorder=sys.byteorder)

red = int.from_bytes(ReadBytes(1), byteorder=sys.byteorder)
green = int.from_bytes(ReadBytes(1), byteorder=sys.byteorder)
blue = int.from_bytes(ReadBytes(1), byteorder=sys.byteorder)
clrrsrvd = int.from_bytes(ReadBytes(1), byteorder=sys.byteorder)
red = int.from_bytes(ReadBytes(1), byteorder=sys.byteorder)
green = int.from_bytes(ReadBytes(1), byteorder=sys.byteorder)
blue = int.from_bytes(ReadBytes(1), byteorder=sys.byteorder)
clrrsrvd = int.from_bytes(ReadBytes(1), byteorder=sys.byteorder)

RIP = 29    # Instruction Register
PS  = 30    # Prime Sequence Register
PR  = 31    # Position Register
registers = [0] * 32

# Initialize Registers
registers[RIP] = dataOffest
registers[PR] = dataOffest
registers[PS] = 0x05030201

print(f'Image Size: {width}x{height}')
print(f'Data Offset: {hex(dataOffest)}')
print('')
print(f'{hsize} {width} {height} {hplanes} {bpx} {hcomp} {isize} {XpixelsPerM} {YpixelsPerM} {colorsUsed} {colorsImportant} {red} {green} {blue} {clrrsrvd}')

memory[0x2E] = (2).to_bytes(1, 'little')
memory[0x1C] = (1).to_bytes(1, 'little')
memory[0x26] = (254).to_bytes(1, 'little')
memory[0x2a] = (254).to_bytes(1, 'little')

def PrintRegisters():
    global memptr, registers, memory
    print(f'PS: {registers[PS]} RIP: {registers[RIP]} PR: {registers[PR]}')
    prtstr = ''
    for i in range(29):
        prtstr += f'R{i}: {registers[i]} '
    print(prtstr)

def PrintInstruction(binn):
    opcode = int(binn[0:4], 2)
    reg1 = int(binn[4:9], 2)

    sInstr = INSTR[opcode]
        

    if sInstr == 'DEAL' or sInstr == 'DEALW' or sInstr == 'WIPE' or sInstr == 'NEGATE' or sInstr == 'SWAP' or sInstr == 'DRAW' or sInstr == 'DRAWW' or sInstr == 'JUMP':
        reg = f'R{reg1}'
        if reg1 == RIP:
            reg = f'RIP'
        elif reg1 == PR:
            reg = f'PR'
        elif reg1 == PS:
            reg = f'PS'
        print(f'{INSTR[opcode]}  {reg}\t\t\t({binn})')
    elif sInstr == 'COPY4':
        reg2 = int(binn[9:14], 2)
        regA = f'R{reg1}'
        if reg1 == RIP:
            regA = f'RIP'
        elif reg1 == PR:
            regA = f'PR'
        elif reg1 == PS:
            regA = f'PS'

        regB = f'R{reg2}'
        if reg2 == RIP:
            regB = f'RIP'
        elif reg2 == PR:
            regB = f'PR'
        elif reg2 == PS:
            regB = f'PS'

        b1 = int(binn[14])
        b2 = int(binn[15])
        b3 = int(binn[16])
        b4 = int(binn[17])

        print(f'{INSTR[opcode]} {regA} {regB} {b1}{b2}{b3}{b4}\t\t({binn})')
    elif sInstr == 'LOADI':
        imm = int(binn[9:25], 2)
        regA = f'R{reg1}'
        if reg1 == RIP:
            regA = f'RIP'
        elif reg1 == PR:
            regA = f'PR'
        elif reg1 == PS:
            regA = f'PS'

        print(f'{INSTR[opcode]} {regA} {imm}\t\t\t({binn})')
    elif sInstr == 'XOR' or sInstr == 'ADD':
        reg2 = int(binn[9:14], 2)
        reg3 = int(binn[14:19], 2)

        regA = f'R{reg1}'
        if reg1 == RIP:
            regA = f'RIP'
        elif reg1 == PR:
            regA = f'PR'
        elif reg1 == PS:
            regA = f'PS'

        regB = f'R{reg2}'
        if reg2 == RIP:
            regB = f'RIP'
        elif reg2 == PR:
            regB = f'PR'
        elif reg2 == PS:
            regB = f'PS'

        regC = f'R{reg3}'
        if reg3 == RIP:
            regC = f'RIP'
        elif reg3 == PR:
            regC = f'PR'
        elif reg3 == PS:
            regC = f'PS'

        print(f'{INSTR[opcode]} {regA} {regB} {regC}\t\t\t({binn})')
    elif sInstr == 'HALT':
        print(f'{INSTR[opcode]}\t\t\t\t({binn}')
    elif sInstr == 'LOADB' or sInstr == 'STOREB':
        reg2 = int(binn[9:14], 2)
        imm = int(binn[9:25], 2)

        regA = f'R{reg1}'
        if reg1 == RIP:
            regA = f'RIP'
        elif reg1 == PR:
            regA = f'PR'
        elif reg1 == PS:
            regA = f'PS'

        regB = f'R{reg2}'
        if reg2 == RIP:
            regB = f'RIP'
        elif reg2 == PR:
            regB = f'PR'
        elif reg2 == PS:
            regB = f'PS'

        print(f'{INSTR[opcode]} {regA} {regB} {imm}\t\t({binn})')
    else:
        print(sInstr + ' ' + binn)

def Disassemble():
    global memptr, registers, memory
    print('--- Disassembly ---')
    memptr = dataOffest
    isRunning = True
    counter = dataOffest
    while isRunning:
        binn = bin(int.from_bytes(ReadBytes(4), byteorder='big'))[2:].zfill(32)
    
        PrintInstruction(binn)
        counter += 4
        if counter > len(memory):
            isRunning = False

    PrintRegisters()

def Step():
    global memptr, registers, memory
    memptr = registers[RIP]
    binn = bin(int.from_bytes(ReadBytes(4), byteorder='big'))[2:].zfill(32)
    opcode = int(binn[0:4], 2)
    reg1 = int(binn[4:9], 2)

    sInstr = INSTR[opcode]

    if sInstr != 'JUMP':
        registers[RIP] = registers[RIP] + 4

    PrintInstruction(binn)
    if sInstr == 'COPY4':
        reg1 = int(binn[4:9], 2)
        reg2 = int(binn[9:14], 2)
        mask = int(binn[14:18], 2)
        
        registers[reg1] = (registers[reg1] & (~(1 << 0))) | (registers[reg2] & 1)
        registers[reg1] = (registers[reg1] & (~(1 << 1))) | (registers[reg2] & 2)
        registers[reg1] = (registers[reg1] & (~(1 << 2))) | (registers[reg2] & 4)
        registers[reg1] = (registers[reg1] & (~(1 << 3))) | (registers[reg2] & 10)


    elif sInstr == 'LOADI':
        reg1 = int(binn[4:9], 2)
        imm = int(binn[9:25], 2)
        registers[reg1] = (registers[reg1] & (0xFFFF0000)) | imm
    elif sInstr == 'ADD':
        reg1 = int(binn[4:9], 2)
        reg2 = int(binn[9:14], 2)
        reg3 = int(binn[14:19], 2)

        registers[reg3] = registers[reg1] + registers[reg2]
    elif sInstr == 'NEGATE':
        registers[reg1] = -1 * registers[reg1]
    elif sInstr == 'DRAWW':
        reg1 = int(binn[4:9], 2)

        registers[reg1] = int.from_bytes(ReadBytesAt(4, registers[PR]), byteorder='big')
        del(memory[registers[PR]])
        del(memory[registers[PR]])
        del(memory[registers[PR]])
        del(memory[registers[PR]])

        # Unchanged
        registers[PR] = registers[PR]
        registers[RIP] = registers[RIP]
    elif sInstr == 'DRAW':
        reg1 = int(binn[4:9], 2)

        registers[reg1] = ((registers[reg1] << 8) & 0xFFFFFFFF) | int.from_bytes(ReadBytesAt(1, registers[PR]), byteorder='big')
        del(memory[registers[PR]])


        # Unchanged
        registers[PR] = registers[PR]
        registers[RIP] = registers[RIP]
    elif sInstr == 'DEAL':
        reg1 = int(binn[4:9], 2)
        memory.insert(registers[PR], 0)
        val = registers[reg1] >> 24
        memory[registers[PR]] = val.to_bytes(1, 'big')

        if registers[RIP] > registers[PR]:
            registers[RIP] = registers[RIP] + 1
        registers[PR] = registers[PR] + 1
        registers[reg1] = (registers[reg1] << 8) & 0xFFFFFFFF
    elif sInstr == 'DEALW':
        reg1 = int(binn[4:9], 2)

        if registers[reg1] < 0:
            registers[reg1] = registers[reg1] & 0xFFFFFFFF

        memory.insert(registers[PR], 0)
        memory.insert(registers[PR], 0)
        memory.insert(registers[PR], 0)
        memory.insert(registers[PR], 0)


        val = (registers[reg1] >> 0) & 0xFF
        memory[registers[PR] + 3] = val.to_bytes(1, 'big')
        val = (registers[reg1] >> 8) & 0xFF
        memory[registers[PR] + 2] = val.to_bytes(1, 'big')
        val = (registers[reg1] >> 16) & 0xFF
        memory[registers[PR] + 1] = val.to_bytes(1, 'big')
        val = (registers[reg1] >> 24) & 0xFF
        memory[registers[PR] + 0] = val.to_bytes(1, 'big')

        if registers[RIP] > registers[PR]:
            registers[RIP] = registers[RIP] + 4
        registers[PR] = registers[PR] + 4
        registers[reg1] = 0
    elif sInstr == 'LOADB':
        reg1 = int(binn[4:9], 2)
        reg2 = int(binn[9:14], 2)
        imm = int(binn[14:30], 2)

        registers[reg1] = (registers[reg1] & 0xFFFFFF00) | int.from_bytes(ReadBytesAt(1, registers[reg2] + imm), byteorder='big')

    elif sInstr == 'JUMP':
        reg1 = int(binn[4:9], 2)
        registers[RIP] = registers[reg1]
    elif sInstr == 'WIPE':
        reg1 = int(binn[4:9], 2)
        val = 0
        registers[reg1] = val.to_bytes(1, 'big')
    elif sInstr == 'XOR':
        reg1 = int(binn[4:9], 2)
        reg2 = int(binn[9:14], 2)
        reg3 = int(binn[14:19], 2)

        registers[reg3] = registers[reg1] ^ registers[reg2]
    elif sInstr == 'SWAP':
        reg1 = int(binn[4:9], 2)

        most = registers[reg1] >> 24
        least = registers[reg1] & 0xFF

        registers[reg1] = (registers[reg1] & 0xFFFFFF00) | most
        registers[reg1] = (registers[reg1] & 0x00FFFFFF) | least

    elif sInstr == 'HALT':
        print('----------\nProgram Exited\n----------')
        return -1
    else:
        print('UNKNOWN INSTRUCTION')
        print(sInstr)


    PrintRegisters()
    return 0


while True:
    print('D (Disassemble), S (Step), E (Exit)')
    inp = input()
    if inp == 'd':
        Disassemble()
    elif inp == 's':
        if Step() == -1:
            break
    elif inp == 'e':
        break

while True:
    if Step() == -1:
        break

out = open('bmpx/solve.bmpx', 'wb+')
for i in range(len(memory)):
    out.write(memory[i])