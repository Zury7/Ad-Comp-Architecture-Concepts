from collections import deque

class Instruction:
    def __init__(self, name, op, src1=None, src2=None, dest=None):
        self.name = name
        self.op = op
        self.src1 = src1
        self.src2 = src2
        self.dest = dest
        self.executed = False
        self.result = None

class SuperscalarPipeline:
    def __init__(self, num_units=4):
        self.fetch_buffer = deque()  # IF stage
        self.decode_buffer = deque()  # ID stage
        self.dispatch_buffer = deque()  # RD stage
        self.functional_units = {f"FU{i}": None for i in range(num_units)}  # EX stage
        self.reorder_buffer = deque()  # ROB for in-order WB
        self.clock = 0

    def fetch(self, instructions):
        # Fetch up to 2 instructions per cycle
        for _ in range(2):
            if instructions:
                self.fetch_buffer.append(instructions.pop(0))

    def decode(self):
        # Decode up to 2 instructions per cycle
        for _ in range(2):
            if self.fetch_buffer:
                instr = self.fetch_buffer.popleft()
                self.decode_buffer.append(instr)

    def dispatch(self):
        # Dispatch up to 2 instructions per cycle
        for _ in range(2):
            if self.decode_buffer:
                instr = self.decode_buffer.popleft()
                self.dispatch_buffer.append(instr)

    def execute(self):
        # Execute instructions out of order in functional units
        for unit, instr in self.functional_units.items():
            if instr and not instr.executed:
                if instr.op == "ADD":
                    instr.result = instr.src1 + instr.src2
                elif instr.op == "SUB":
                    instr.result = instr.src1 - instr.src2
                elif instr.op == "MUL":
                    instr.result = instr.src1 * instr.src2
                elif instr.op == "DIV":
                    instr.result = instr.src1 / instr.src2
                instr.executed = True
                print(f"{instr.name} executed on {unit} with result: {instr.result}")
                self.reorder_buffer.append(instr)
                self.functional_units[unit] = None

        # Dispatch instructions to available functional units
        for unit, instr in self.functional_units.items():
            if not instr and self.dispatch_buffer:
                self.functional_units[unit] = self.dispatch_buffer.popleft()

    def write_back(self):
        # Write results back in program order
        if self.reorder_buffer:
            instr = self.reorder_buffer.popleft()
            print(f"{instr.name} written back with result: {instr.result}")

    def run(self, instructions):
        while instructions or self.fetch_buffer or self.decode_buffer or self.dispatch_buffer or any(self.functional_units.values()) or self.reorder_buffer:
            print(f"Clock Cycle: {self.clock}")
            self.write_back()
            self.execute()
            self.dispatch()
            self.decode()
            self.fetch(instructions)
            self.clock += 1

# Example Instructions
instructions = [
    Instruction("I1", "ADD", 3, 5, "R1"),
    Instruction("I2", "SUB", 8, 2, "R2"),
    Instruction("I3", "MUL", 6, 7, "R3"),
    Instruction("I4", "DIV", 10, 2, "R4"),
]

# Simulate Pipeline
pipeline = SuperscalarPipeline(num_units=3)
pipeline.run(instructions)
