import queue

class ReservationStation:
    def __init__(self, name):
        self.name = name
        self.busy = False
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.result = None

class Register:
    def __init__(self):
        self.value = None
        self.reservation_station = None

class Tomasulo:
    def __init__(self, num_stations=3, num_registers=8):
        self.reservation_stations = [ReservationStation(f"RS{i}") for i in range(num_stations)]
        self.register_file = {f"R{i}": Register() for i in range(num_registers)}
        self.instruction_queue = queue.Queue()
        self.clock = 0
        self.instructions = []

    def add_instruction(self, op, dest, src1, src2):
        self.instructions.append((op, dest, src1, src2))
        self.instruction_queue.put((op, dest, src1, src2))

    def issue(self):
        if self.instruction_queue.empty():
            return

        op, dest, src1, src2 = self.instruction_queue.get()
        for rs in self.reservation_stations:
            if not rs.busy:
                rs.busy = True
                rs.op = op
                rs.qj = self.register_file[src1].reservation_station
                rs.qk = self.register_file[src2].reservation_station
                rs.vj = self.register_file[src1].value if rs.qj is None else None
                rs.vk = self.register_file[src2].value if rs.qk is None else None
                self.register_file[dest].reservation_station = rs.name
                print(f"Issued {op} {dest}, {src1}, {src2} to {rs.name}")
                break

    def execute(self):
        for rs in self.reservation_stations:
            if rs.busy and rs.qj is None and rs.qk is None:
                if rs.op == "ADD":
                    rs.result = rs.vj + rs.vk
                elif rs.op == "SUB":
                    rs.result = rs.vj - rs.vk
                elif rs.op == "MUL":
                    rs.result = rs.vj * rs.vk
                elif rs.op == "DIV":
                    rs.result = rs.vj / rs.vk
                print(f"Executing {rs.op} in {rs.name}, result: {rs.result}")
                rs.busy = False

    def write_back(self):
        for rs in self.reservation_stations:
            if rs.result is not None:
                for reg in self.register_file.values():
                    if reg.reservation_station == rs.name:
                        reg.value = rs.result
                        reg.reservation_station = None
                        print(f"Written back result {rs.result} to register")
                rs.result = None

    def run(self):
        while not self.instruction_queue.empty() or any(rs.busy for rs in self.reservation_stations):
            print(f"Clock Cycle: {self.clock}")
            self.issue()
            self.execute()
            self.write_back()
            self.clock += 1

# Test Run
tomasulo = Tomasulo()
tomasulo.add_instruction("ADD", "R1", "R2", "R3")
tomasulo.add_instruction("SUB", "R4", "R5", "R6")
tomasulo.add_instruction("MUL", "R7", "R1", "R4")
tomasulo.run()
