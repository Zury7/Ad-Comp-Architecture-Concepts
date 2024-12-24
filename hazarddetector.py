class Instruction:
    def __init__(self, name, operation, dest=None, src1=None, src2=None):
        self.name = name  # Instruction name (e.g., "I1")
        self.operation = operation  # Operation type (e.g., "ADD", "SUB")
        self.dest = dest  # Destination register
        self.src1 = src1  # First source register
        self.src2 = src2  # Second source register


def detect_raw_hazards(instructions):
    raw_hazards = []
    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            instr1 = instructions[i]
            instr2 = instructions[j]
            if instr1.dest and (instr1.dest == instr2.src1 or instr1.dest == instr2.src2):
                raw_hazards.append((instr1.name, instr2.name))
    return raw_hazards


def detect_war_hazards(instructions):
    war_hazards = []
    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            instr1 = instructions[i]
            instr2 = instructions[j]
            if instr2.dest and (instr2.dest == instr1.src1 or instr2.dest == instr1.src2):
                war_hazards.append((instr1.name, instr2.name))
    return war_hazards


def detect_waw_hazards(instructions):
    waw_hazards = []
    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            instr1 = instructions[i]
            instr2 = instructions[j]
            if instr1.dest and instr2.dest and instr1.dest == instr2.dest:
                waw_hazards.append((instr1.name, instr2.name))
    return waw_hazards


# Example instructions
instructions = [
    Instruction("I1", "ADD", dest="R1", src1="R2", src2="R3"),
    Instruction("I2", "SUB", dest="R4", src1="R1", src2="R5"),
    Instruction("I3", "MUL", dest="R1", src1="R6", src2="R7"),
    Instruction("I4", "DIV", dest="R2", src1="R1", src2="R4"),
]

# Detect hazards
raw_hazards = detect_raw_hazards(instructions)
war_hazards = detect_war_hazards(instructions)
waw_hazards = detect_waw_hazards(instructions)

# Print detected hazards
print("RAW Hazards (Read After Write):")
for hazard in raw_hazards:
    print(f"{hazard[0]} -> {hazard[1]}")

print("\nWAR Hazards (Write After Read):")
for hazard in war_hazards:
    print(f"{hazard[0]} -> {hazard[1]}")

print("\nWAW Hazards (Write After Write):")
for hazard in waw_hazards:
    print(f"{hazard[0]} -> {hazard[1]}")
