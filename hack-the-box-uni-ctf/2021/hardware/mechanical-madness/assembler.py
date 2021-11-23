# assembler.py
input = open('program.asm', 'r')
out = open('program.data', 'w+')

binary = []

# opcodes
opcodes = {
    'movl' : 0x10,
    'clr' : 0x03,
    'mmiv' : 0x17,
    'mmov' : 0x18,
    'call' : 0x11,
    'push' : 0x14,
    'sub' : 0x01,
    'cmp' : 0x13,
    'jnz' : 0x0e,
    'pop' : 0x15,
    'msk' : 0x1a,
    'mskb' : 0x1b,
    'jl' : 0x0a,
    'jmp' : 0x05,
    'ret' : 0x12
}

# registers
registers = {
    'ax' : 0x00,
    'bx' : 0x01,
    'cx' : 0x02,
    'dx' : 0x03
}

labels = {}

def make_operand(operand):
    # If addition on label
    if len(operand.split('+')) == 2:
        arr = operand.split('+')
        return str(hex(labels[arr[0]] + int(arr[1], 10))[2:]).zfill(2)

    # Convert depending on type
    if operand in registers:
        return str(hex(registers[operand])[2:]).zfill(2)
    elif operand in labels:
        return str(hex(labels[operand])[2:]).zfill(2)
    elif operand.startswith('0x'):
        return str(hex(int(operand, 16))[2:]).zfill(2)
    elif operand.isnumeric:
        return str(hex(int(operand, 10))[2:]).zfill(2)
    else:
        return str(hex(int(operand, 16))[2:]).zfill(2)
        
def parse_labels(lines):
    instruction_counter = 0
    for line in lines:
        l = line.strip()
        
        # parse labels
        if l.startswith(':'):
            labels[l] = instruction_counter
            continue
            
        instruction_counter += 1
    return
    
def compile():
    out.write('v2.0 raw\n')
    for instr in binary:
        out.write(instr + ' ')
    return

def parse():
    instruction_counter = 0
    lines = input.readlines()
    parse_labels(lines)
    print(labels)
    for line in lines:
        l = line.strip()

        if l.startswith(':'):
            continue

        instruction = ''
        opcode = l.split(' ')[0]
        instruction += str(hex(opcodes[opcode])[2:])
        
        # remove empty spaces
        args = [x.replace(',', '') for x in l.split(' ') if x != '']
        
        # check if instruction with no args
        if len(args) != 1:
            instruction += make_operand(args[1])
            instruction += make_operand(args[2])        
        else:
            instruction += '0000'
        
        binary.append(instruction)
        instruction_counter += 1
        

parse()
compile()
#print(labels)