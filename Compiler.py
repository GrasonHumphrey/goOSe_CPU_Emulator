

# All values must be in hex
# # for comment

# SET sets value in memory
# LOC defines a location in code for looping etc
# DEF defines a macro variable (can be 8 or 16 bit)
# HERE statically sets the location of the next command in memory (use with caution, may skip memory locations)

# TODO: Auto variable memory location assignment








code = """
# Python line 21

DEF sp1 *80
DEF sp2 *81
DEF reta *82
DEF retb *83
DEF tempa *84
DEF tempb *85
DEF op1 *86
DEF op2 *87

#SET sp1 90
#SET sp2 0
#SET op1 7
#SET op2 9

#PUSH sp1 sp2 op1
#PUSH sp1 sp2 op2
#GADD

DEF count *50
DEF sum *51

MOV AR 5

LOC loop
MOV count AR

MOV AR sum
#IO AR
ADD A
#IO AR
MOV sum AR

MOV AR count
DEC AR
#IO AR

JNZ loop

MOV AR sum

HALT



"""

# POP(*sp1, *sp2, *ret)
POP = """
# Save A and B to temp regs
MOV tempa A
MOV tempb B
# Load sp values
MOV A sp1
MOV B sp2
# Get value at sp and save to ret
LDAB
MOV ret A
# Decrement sp1
MOV A sp1
DEC A
MOV sp1 A
JNOFO 7
# Decrement sp2 if needed
MOV B sp2
DEC B
MOV sp2 B
# Reload A and B from temp regs
MOV A tempa
MOV B tempb
"""

# PUSH (*sp1, *sp2, *val)
PUSH = """
# Save A and B to temp regs
MOV tempa A
MOV tempb B
# Increment sp1
MOV A sp1
MOV B sp2
INC A
MOV sp1 A
JNOFO 4
# Increment sp2 if needed
INC B
MOV sp2 B
# Save value to given sp
STOAB val
# Reload A and B from temp regs
MOV A tempa
MOV B tempb
"""





output = ""

cmdNum = 0
lowestSet = -1
setVars = []
cmdBytes = []
expectArgs = 0

hexChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

locVars = [[], []]
defVars = [[], []]
totalVars = []


def throwError(description, line):
    print("ERROR: " + description + "  |  line: " + str(line+1))
    quit()
    return


def gen_cmd(data, outLine):
    return "memory[" + str(outLine) + "] <= 8'h" + data + ";\n"

def gen_cmd_file(data, outLine):
    return str(outLine) + " " + data + "\n"


def clean_operand(op, line):
    cleanOp = op
    if (not op in totalVars):
        if (op[0] == "*"):
            cleanOp = cleanOp[1:]
            if (len(cleanOp) > 4):
                throwError("Bad memory operand length (Memory addresses be 4 nibbles, detected: " + str(len(cleanOp)) + ")", line)
            for i in range(4 - len(cleanOp)):
                cleanOp = "0" + cleanOp;
        else:
            if (len(cleanOp) > 2):
                throwError("Bad data operand length (Data must be 2 nibbles, detected: " + str(len(cleanOp)) + ")", line)
            for i in range(2 - len(cleanOp)):
                cleanOp = "0" + cleanOp;

        for i in range(len(cleanOp)):
            if (not(cleanOp[i] in hexChars)):
                throwError("Invalid hex character: " + cleanOp[i], line)

    return cleanOp

codeParts = code.lower().split("\n")[1:-1]

for line in range(len(codeParts)):
    lineParts = codeParts[line].split()
    ops = []
    if (len(lineParts) != 0):
        if (lineParts[0][0] != '#'):

            for op in range(len(lineParts)):
                ops.append(lineParts[op])
                        
            if (ops[0] == "loc"):
                expectArgs = 2
                if (not (ops[1] in locVars[0])):
                    if "." not in ops[1]:
                        if "*" not in ops[1]:
                            locVars[0].append(ops[1])
                            locVars[1].append(ops[1])
                            totalVars.append(ops[1])
                        else:
                            throwError("Invalid character '*' in LOC variable: " + ops[1], line)
                    else:
                        throwError("Invalid character '.' in LOC variable: " + ops[1], line)
                else:
                    throwError("More than one LOC variable given same name: " + ops[1], line)

            elif (ops[0] == "def"):
                expectArgs = 3
                if (not (ops[1] in defVars[0])):
                    if "." not in ops[1]:
                        if "*" not in ops[1]:
                            defVars[0].append(ops[1])
                            defVars[1].append(str(ops[2]))
                            totalVars.append(ops[1])
                        else:
                            throwError("Invalid character '*' in DEF variable: " + ops[1], line) 
                    else:
                         throwError("Invalid character '.' in DEF variable: " + ops[1], line)   
                else:
                    throwError("More than one DEF variable given same name: " + ops[1], line)

            elif (ops[0] == "pop"):
                if (len(ops) != 4):
                    throwError("POP needs 3 arguments, given: " + str(len(ops)-1), line)
                customPop = POP.replace("sp1", ops[1]).replace("sp2", ops[2]).replace("ret", ops[3])
                code = code.lower().replace(codeParts[line], customPop, 1)
                print(code)

            elif (ops[0] == "push"):
                if (len(ops) != 4):
                    throwError("PUSH needs 3 arguments, given: " + str(len(ops)-1), line)
                customPush = PUSH.replace("sp1", ops[1]).replace("sp2", ops[2]).replace("val", ops[3])
                code = code.lower().replace(codeParts[line], customPush, 1)
                print(code)
    

codeParts = code.lower().split("\n")[1:-1]
for line in range(len(codeParts)):

    lineParts = codeParts[line].split()
    ops = []
    if (len(lineParts) != 0):
        if (lineParts[0][0] != '#'):
            #if (len(lineParts) > 3):
            #    throwError("Incorrect # of line arguments (Max 3 arguments, detected: " + str(len(lineParts)) + ")", line)
            for op in range(len(lineParts)):
                ops.append(lineParts[op])
                
            cleanOp = ""
            opcodeNum = ""

            for op in range(1, len(ops)):
                if (ops[op] in defVars[0]):
                    ops[op] = defVars[1][defVars[0].index(ops[op])]

            if (ops[0] == "mov"):
                # Move operation
                expectArgs = 3
                if (ops[1] == "ar"):
                    # Move into A reg
                    if (ops[2][0] == "*"):
                        # MOV A, [<mem>]
                        cmdBytes.append("01")
                        cmdBytes.append(clean_operand(ops[2], line))
                    else:
                        # MOV A, [<immed>]
                        cmdBytes.append("03")
                        cmdBytes.append(clean_operand(ops[2], line))
                elif (ops[1] == "br"):
                    # Move into B reg
                    if (ops[2][0] == "*"):
                        # MOV B, [<mem>]
                        cmdBytes.append("02")
                        cmdBytes.append(clean_operand(ops[2], line))
                    else:
                        # MOV B, [<immed>]
                        cmdBytes.append("04")
                        cmdBytes.append(clean_operand(ops[2], line))            
                elif (ops[2] == "ar"):
                    # MOV [<mem>], A
                    if (ops[1][0] != "*"):
                        throwError("Must specify a memory address for MEM store operation", line)
                    cmdBytes.append("05")
                    cmdBytes.append(clean_operand(ops[1], line)) 
                elif (ops[2] == "br"):
                    # MOV [<mem>], B
                    if (ops[1][0] != "*"):
                        throwError("Must specify a memory address for MEM store operation", line)
                    cmdBytes.append("06")
                    cmdBytes.append(clean_operand(ops[1], line)) 
                else:
                    throwError("Invalid MOV (invalid register)", line)

            elif (ops[0] == "add"):
                expectArgs = 2
                if (ops[1] == "br"):
                    # ADD B
                    cmdBytes.append("14")
                elif (ops[1][0] == "*"):
                    # ADD [<mem>]
                    cmdBytes.append("11")
                    cmdBytes.append(clean_operand(ops[1], line)) 
                else:
                    # ADD <immed>
                    cmdBytes.append("13")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "sub"):
                expectArgs = 2
                if (ops[1] == "br"):
                    # SUB B
                    cmdBytes.append("44")
                elif (ops[1][0] == "*"):
                    # SUB [<mem>]
                    cmdBytes.append("41")
                    cmdBytes.append(clean_operand(ops[1], line))
                else:
                    # SUB <immed>
                    cmdBytes.append("43")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "jmp"):
                # Unconditional jump
                expectArgs = 2
                if ((ops[1][0] == "*") or (ops[1] in totalVars)):
                    cmdBytes.append("81")
                    cmdBytes.append(clean_operand(ops[1], line))
                else:
                    throwError("Can only jump to memory location", line)

            elif (ops[0] == "jmpo"):
                # Unconditional jump to offset
                expectArgs = 2
                if (ops[1][0] == "*"):
                    throwError("Cannot offset jump to memory location", line)
                else:
                    cmdBytes.append("83")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "jz"):
                # Jump if zero
                expectArgs = 2
                if (ops[1][0] == "*") or (ops[1] in totalVars):
                    cmdBytes.append("91")
                    cmdBytes.append(clean_operand(ops[1], line))
                else:
                    throwError("Can only jump to memory location", line)

            elif (ops[0] == "jzo"):
                # Jump if zero to offset
                expectArgs = 2
                if (ops[1][0] == "*"):
                    throwError("Cannot offset jump to memory location", line)
                else:
                    cmdBytes.append("93")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "jnz"):
                # Jump if not zero
                expectArgs = 2
                if (ops[1][0] == "*") or (ops[1] in totalVars):
                    cmdBytes.append("a1")
                    cmdBytes.append(clean_operand(ops[1], line))
                else:
                    throwError("Can only jump to memory location", line)

            elif (ops[0] == "jnzo"):
                # Jump if not zero to offset
                expectArgs = 2
                if (ops[1][0] == "*"):
                    throwError("Cannot offset jump to memory location", line)
                else:
                    cmdBytes.append("a3")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "jm"):
                # Jump if not positive
                expectArgs = 2
                if (ops[1][0] == "*") or (ops[1] in totalVars):
                    cmdBytes.append("b1")
                    cmdBytes.append(clean_operand(ops[1], line))
                else:
                    throwError("Can only jump to memory location", line)

            elif (ops[0] == "jmo"):
                # Jump if not positive to offset
                expectArgs = 2
                if (ops[1][0] == "*"):
                    throwError("Cannot offset jump to memory location", line)
                else:
                    cmdBytes.append("b3")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "jp"):
                # Jump if positive
                expectArgs = 2
                if (ops[1][0] == "*") or (ops[1] in totalVars):
                    cmdBytes.append("c1")
                    cmdBytes.append(clean_operand(ops[1], line))
                else:
                    throwError("Can only jump to memory location", line)

            elif (ops[0] == "jpo"):
                # Jump if positive to offset
                expectArgs = 2
                if (ops[1][0] == "*"):
                    throwError("Cannot offset jump to memory location", line)
                else:
                    cmdBytes.append("c3")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "jc"):
                # Jump if carry occurred
                expectArgs = 2
                if (ops[1][0] == "*") or (ops[1] in totalVars):
                    cmdBytes.append("d1")
                    cmdBytes.append(clean_operand(ops[1], line))
                else:
                    throwError("Can only jump to memory location", line)

            elif (ops[0] == "jco"):
                # Jump if carry occurred to offset
                expectArgs = 2
                if (ops[1][0] == "*"):
                    throwError("Cannot offset jump to memory location", line)
                else:
                    cmdBytes.append("d3")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "jnc"):
                # Jump if cary did not occur
                expectArgs = 2
                if (ops[1][0] == "*") or (ops[1] in totalVars):
                    cmdBytes.append("e1")
                    cmdBytes.append(clean_operand(ops[1], line))
                else:
                    throwError("Can only jump to memory location", line)

            elif (ops[0] == "jnco"):
                # Jump if cary did not occur to offset
                expectArgs = 2
                if (ops[1][0] == "*"):
                    throwError("Cannot offset jump to memory location", line)
                else:
                    cmdBytes.append("e3")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "jof"):
                # Jump if overflow occurred
                expectArgs = 2
                if (ops[1][0] == "*") or (ops[1] in totalVars):
                    cmdBytes.append("d2")
                    cmdBytes.append(clean_operand(ops[1], line))
                else:
                    throwError("Can only jump to memory location", line)

            elif (ops[0] == "jofo"):
                # Jump if overflow occurred to offset
                expectArgs = 2
                if (ops[1][0] == "*"):
                    throwError("Cannot offset jump to memory location", line)
                else:
                    cmdBytes.append("d4")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "jnof"):
                # Jump if overflow did not occur
                expectArgs = 2
                if (ops[1][0] == "*") or (ops[1] in totalVars):
                    cmdBytes.append("e2")
                    cmdBytes.append(clean_operand(ops[1], line))
                else:
                    throwError("Can only jump to memory location", line)

            elif (ops[0] == "jnofo"):
                # Jump if overflow did not occur to offset
                expectArgs = 2
                if (ops[1][0] == "*"):
                    throwError("Cannot offset jump to memory location", line)
                else:
                    cmdBytes.append("e4")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "shl"):
                # Left shift
                expectArgs = 1
                cmdBytes.append("28")

            elif (ops[0] == "shr"):
                # Right shift
                expectArgs = 1
                cmdBytes.append("29")

            elif (ops[0] == "and"):
                expectArgs = 2
                if (ops[1] == "br"):
                    # AND B
                    cmdBytes.append("21")
                elif (ops[1][0] == "*"):
                    throwError("Cannot AND with memory location", line) 
                else:
                    # ADD <immed>
                    cmdBytes.append("25")
                    cmdBytes.append(clean_operand(ops[1], line))


            elif (ops[0] == "or"):
                expectArgs = 2
                if (ops[1] == "br"):
                    # OR B
                    cmdBytes.append("22")
                elif (ops[1][0] == "*"):
                    throwError("Cannot OR with memory location", line) 
                else:
                    # OR <immed>
                    cmdBytes.append("26")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "xor"):
                expectArgs = 2
                if (ops[1] == "br"):
                    # XOR B
                    cmdBytes.append("23")
                elif (ops[1][0] == "*"):
                    throwError("Cannot XOR with memory location", line) 
                else:
                    # XOR <immed>
                    cmdBytes.append("27")
                    cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "not"):
                # Bitwise NOT
                expectArgs = 1
                cmdBytes.append("24")
                
            elif (ops[0] == "dec"):
                expectArgs = 2
                if(ops[1] == "ar"):
                    cmdBytes.append("2a")
                elif (ops[1] == "br"):
                    cmdBytes.append("2b")
                else:
                    throwError("Invalid reg to decrement: " + ops[1], line)

            elif (ops[0] == "inc"):
                expectArgs = 2
                if(ops[1] == "ar"):
                    cmdBytes.append("2c")
                elif (ops[1] == "br"):
                    cmdBytes.append("2d")
                else:
                    throwError("Invalid reg to decrement: " + ops[1], line)

            elif (ops[0] == "swp"):
                expectArgs = 1
                cmdBytes.append("07")

            elif (ops[0] == "sadd"):
                expectArgs = 1
                cmdBytes.append("09")

            elif (ops[0] == "gadd"):
                expectArgs = 1
                cmdBytes.append("08")

            elif (ops[0] == "stoab"):
                expectArgs = 2
                cmdBytes.append("0a")
                cmdBytes.append(clean_operand(ops[1], line))

            elif (ops[0] == "ldab"):
                expectArgs = 1
                cmdBytes.append("0b")

            elif (ops[0] == "halt"):
                expectArgs = 1
                cmdBytes.append("ff")
                        
            elif (ops[0] == "io"):
                # IO operation
                expectArgs = 2
                if (ops[1] == "ar"):
                    # Display MEMA
                    cmdBytes.append("31")
                elif (ops[1] == "br"):
                    # Display MEMB
                    cmdBytes.append("32")
                else:
                    throwError("Invalid IO (invalid register)", line)

            elif (ops[0] == "set"):
                # Set a memory location directly
                expectArgs = 3
                cleanOp1 = clean_operand(ops[1], line)
                cleanOp1 = str(int(("0x" + cleanOp1), 16))
                cleanOp2 = clean_operand(ops[2], line)
                outLine = int(cleanOp1)
                output += gen_cmd_file(cleanOp2, outLine)
                if (not (outLine in setVars)):
                    setVars.append(outLine)
                else:
                    throwError("Multiple SET commands to same location", line)
                if (outLine <= cmdNum):
                    throwError("SET overwrote compiled code", line)

            elif (ops[0] == "here"):
                expectArgs == 2
                if (not (ops[1][0] == "*")):
                    throwError("HERE must assign a memory location", line)
                else:
                    cleanOp1 = clean_operand(ops[1], line)
                    newCmdNum = int(("0x" + cleanOp1), 16)
                    if (newCmdNum < cmdNum):
                        throwError("HERE overwrote compiled code", line)
                    elif (newCmdNum in setVars):
                        throwError("HERE overwrote SET variable", line)
                    else:
                        cmdNum = newCmdNum

            elif (ops[0] == "loc"):
                expectArgs = 2
                index1 = locVars[0].index(ops[1])
                cleanCmdNum = clean_operand("*" + str(hex(cmdNum)).replace("0x", ""), line)
                locVars[1][index1] = cleanCmdNum

            elif (ops[0] == "def"):
                expectArgs = 3
                #if (not (ops[1] in locVars[0])):
                #    locVars[0].append(ops[1])
                #    locVars[1].append(str(ops[2]))
                #else:
                #    throwError("More than one variable given same name: " + ops[1], line)
                    
            else:
                throwError("Invalid ops[0]: " + ops[0], line)


            if (not((ops[0] == "set") or (ops[0] == "loc") or (ops[0] == "def") or (ops[0] == "here"))):
                if (cmdNum in setVars):
                    throwError("Compiled code overwrote SET on cmdNum: " + str(cmdNum), line)
                if (len(lineParts) != expectArgs):
                    throwError("Wrong number of operands for ops[0]: " + ops[0] + ". Got: " + str(len(lineParts)-1) + ", expected: " + str(expectArgs-1), line)

                for i in range(len(cmdBytes)):        
                    currentCmd = cmdBytes.pop(0)
                    if (not currentCmd in locVars[0]):
                        if len(currentCmd) > 2:
                            if (cmdNum in setVars):
                                throwError("Compiled code overwrote SET on cmdNum: " + str(cmdNum), line)  
                            output += gen_cmd_file(currentCmd[2:4], cmdNum)
                            cmdNum += 1
                        if (cmdNum in setVars):
                            throwError("Compiled code overwrote SET on cmdNum: " + str(cmdNum), line)
                        output += gen_cmd_file(currentCmd[0:2], cmdNum)
                        cmdNum += 1
                    else:
                        output += gen_cmd_file(currentCmd + ".1", cmdNum)
                        cmdNum += 1
                        output += gen_cmd_file(currentCmd + ".2", cmdNum)
                        cmdNum += 1
                         

for locVar in range(len(locVars[0])):
    output = output.replace(locVars[0][locVar] + ".1", locVars[1][locVar][2:4])
    output = output.replace(locVars[0][locVar] + ".2", locVars[1][locVar][0:2])
    
    

print
print("Compilation success.")
print
print(output)
f = open("compiled_output.txt", "w")
f.write(output)
f.close()
